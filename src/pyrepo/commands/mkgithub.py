from typing import Optional
import click
from ..config import Config
from ..project import Project, with_project
from ..util import cpe_no_tb, readcmd, runcmd


@click.command()
@click.option("-P", "--private", is_flag=True, help="Make the new repo private")
@click.option("--repo-name", metavar="NAME", help="Set the name of the repository")
@click.pass_obj
@with_project
@cpe_no_tb
def cli(obj: Config, project: Project, repo_name: Optional[str], private: bool) -> None:
    """Create a repository on GitHub for the local project and upload it"""
    if repo_name is None:
        repo_name = project.repo_name
    repo = obj.gh.user.repos.post(
        json={
            "name": repo_name,
            "description": project.short_description,
            "private": private,
        }
    )
    keywords = [kw.lower().replace(" ", "-") for kw in project.keywords]
    if "python" not in keywords:
        keywords.append("python")
    obj.gh[repo["url"]].topics.put(json={"names": keywords})
    if "origin" in readcmd("git", "remote", cwd=project.directory).splitlines():
        runcmd("git", "remote", "rm", "origin", cwd=project.directory)
    runcmd("git", "remote", "add", "origin", repo["ssh_url"], cwd=project.directory)
    runcmd("git", "push", "-u", "origin", project.default_branch, cwd=project.directory)
