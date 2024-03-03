# from aws_cdk import (
#     aws_codepipeline as codepipeline,
#     aws_codepipeline_actions as codepipeline_actions,
#     aws_codebuild as codebuild,
#     aws_s3 as s3,
#     aws_iam as iam,
#     core
# )


# class MyCodePipelineStack(core.Stack):

#     def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
#         super().__init__(scope, id, **kwargs)

#         # Create an S3 bucket to store the artifacts
#         artifact_bucket = s3.Bucket(
#             self, "MyArtifactBucket",
#             versioned=True
#         )

#         # Create a CodeBuild project
#         code_build_project = codebuild.PipelineProject(
#             self, "MyCodeBuildProject",
#             environment=codebuild.BuildEnvironment(
#                 build_image=codebuild.LinuxBuildImage.STANDARD_4_0,
#                 privileged=True
#             ),
#             environment_variables={
#                 'ENV': codebuild.BuildEnvironmentVariable(value='prod')
#             }
#         )

#         # Grant necessary permissions to CodeBuild project
#         artifact_bucket.grant_read_write(code_build_project)

#         # Create IAM role for the pipeline
#         pipeline_role = iam.Role(
#             self, "MyPipelineRole",
#             assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com"),
#             managed_policies=[
#                 iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
#             ]
#         )

#         # Create the CodePipeline pipeline
#         pipeline = codepipeline.Pipeline(
#             self, "MyPipeline",
#             artifact_bucket=artifact_bucket,
#             role=pipeline_role
#         )

#         # Add source stage to the pipeline
#         github_source_output = codepipeline.Artifact()
#         source_action = codepipeline_actions.GitHubSourceAction(
#             action_name="GitHub_Source",
#             owner="OWNER",
#             repo="REPO",
#             branch="main",
#             oauth_token=core.SecretValue.secrets_manager("my-github-token"),
#             output=github_source_output
#         )

#         pipeline.add_stage(
#             stage_name="Source",
#             actions=[source_action]
#         )

#         # Add build stage to the pipeline
#         build_output = codepipeline.Artifact()
#         build_action = codepipeline_actions.CodeBuildAction(
#             action_name="CodeBuild",
#             input=github_source_output,
#             outputs=[build_output],
#             project=code_build_project
#         )

#         pipeline.add_stage(
#             stage_name="Build",
#             actions=[build_action]
#         )


# app = core.App()
# MyCodePipelineStack(app, "MyCodePipelineStack")
# app.synth()
