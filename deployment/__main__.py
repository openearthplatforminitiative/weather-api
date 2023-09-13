import json

import pulumi
import pulumi_aws as aws


def main():
    common_stack = pulumi.StackReference(f"openepi/infrastructure/{pulumi.get_stack()}")

    vpc_private_subnet_ids = common_stack.require_output("vpc_private_subnet_ids")
    cluster_arn = common_stack.require_output("cluster_arn")
    private_security_group = common_stack.require_output("private_access_sg")

    role = aws.iam.Role(
        "task-exec-role",
        assume_role_policy=json.dumps(
            {
                "Version": "2008-10-17",
                "Statement": [
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                        "Action": "sts:AssumeRole",
                    }
                ],
            }
        ),
    )

    aws.iam.RolePolicyAttachment(
        "task-exec-policy",
        role=role.name,
        policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    )

    log_group_name = "weather-api-log-group"
    aws.cloudwatch.LogGroup(
        log_group_name,
        name=log_group_name,
        retention_in_days=7,  # Set the desired retention period
    )

    task_definition = aws.ecs.TaskDefinition(
        "weather-api-task",
        family="weather-api-task-definition",
        cpu="256",
        memory="512",
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        execution_role_arn=role.arn,
        container_definitions=json.dumps(
            [
                {
                    "name": "weather-api",
                    "image": "ghcr.io/openearthplatforminitiative/weather-api:0.0.2",
                    "portMappings": [
                        {"containerPort": 8080, "hostPort": 8080, "protocol": "tcp"}
                    ],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": log_group_name,
                            "awslogs-region": "eu-central-1",
                            "awslogs-stream-prefix": "weather-api",
                        },
                    },
                    "dockerLabels": {
                        "traefik.enable": "true",
                        "traefik.http.routers.weather-api.rule": "PathPrefix(`/weather`)",
                        "traefik.http.services.weather-api.loadbalancer.server.port": "8080",
                        "traefik.http.middlewares.weather-api-stripprefix.stripprefix.prefixes": "/weather",
                        "traefik.http.routers.weather-api.middlewares": "weather-api-stripprefix@ecs",
                    },
                }
            ]
        ),
    )

    aws.ecs.Service(
        "weather-api-svc",
        cluster=cluster_arn,
        desired_count=1,
        launch_type="FARGATE",
        task_definition=task_definition.arn,
        network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
            assign_public_ip=True,
            subnets=vpc_private_subnet_ids,
            security_groups=[private_security_group],
        ),
    )


if __name__ == "__main__":
    main()
