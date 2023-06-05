from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    Stage,
    Environment,
    pipelines,
    aws_codepipeline as codepipeline
)
from constructs import Construct
from resource_stack.resource_stack import ResourceStack


class DeployStage(Stage):
    def __init__(self, scope: Construct, id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)
        ResourceStack(self, 'ResourceStack', env=env, stack_name="resource-stack-deploy")


class CiCdAwsPipelinePythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        git_input = pipelines.CodePipelineSource.connection(
            repo_string="sumit1912/ci-cd-aws-pipeline-typescript",
            branch="main",
            connection_arn="arn:aws:codestar-connections:eu-central-1:496932237066:connection/54bd73f5-1116-4856-805a-7d8725576248"
        )

        code_pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name="new-pipeline",
            cross_account_keys=False
        )

        synth_step = pipelines.ShellStep(
            id="Synth",
            install_commands=[
                'pip install -r requirements.txt'
            ],
            commands=[
                'npx cdk synth'
            ],
            input=git_input
        )

        pipeline = pipelines.CodePipeline(
            self, 'CodePipeline',
            self_mutation=True,
            code_pipeline=code_pipeline,
            synth=synth_step
        )

        deployment_wave = pipeline.add_wave("DeploymentWave")

        deployment_wave.add_stage(DeployStage(
            self, 'DeployStage',
            env=(Environment(account='496932237066', region='eu-central-1'))
        ))
