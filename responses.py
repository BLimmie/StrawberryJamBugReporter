import os

import discord
from discord import ui, SelectOption, InputTextStyle, Interaction, Embed
from github import Github

BUG_COLOR = 0x117bed
GAMEPLAY_COLOR = 0xf073e7
VISUAL_COLOR = 0x652394
ACCESSIBILITY_COLOR = 0x6cf088
OTHER_COLOR = 0xe81324

color_map = {
    "Bug": BUG_COLOR,
    "Gameplay": GAMEPLAY_COLOR,
    "Visual": VISUAL_COLOR,
    "Accessibility": ACCESSIBILITY_COLOR,
    "Other": OTHER_COLOR,
}


def send_to_github(label, issue_title, issue_desc, issue_links):
    git_token = os.environ["GIT_LOGIN"]
    g = Github(git_token)
    repo = g.get_repo("StrawberryJam2021/StrawberryJamIssues")
    git_label = repo.get_label(label)
    desc = issue_desc + "\n\n" + "Links:\n" + issue_links
    issue = repo.create_issue(issue_title, body=desc, labels=[git_label])
    url = issue.html_url
    return url


class ReportModal(ui.Modal):
    def __init__(self, label, user: discord.User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label
        self.user = user
        self.add_item(ui.InputText(label="Provide a quick summary of the issue", max_length=100, required=True))
        self.add_item(ui.InputText(label="Describe the issue in more detail", style=InputTextStyle.long, required=True))
        self.add_item(
            ui.InputText(label="Provide any additional links to images", style=InputTextStyle.long, required=False))

    async def callback(self, interaction: Interaction):
        issue_title = self.children[0].value
        issue_desc = self.children[1].value
        issue_links = self.children[2].value
        if not issue_links:
            issue_links = "<None>"
        url = send_to_github(self.label, issue_title, issue_desc, issue_links)
        embed = Embed(title=f"{self.label} Issue Reported", color=color_map[self.label])
        embed.add_field(name="Issue Title", value=issue_title, inline=False)
        embed.add_field(name="Issue Description", value=issue_desc, inline=False)
        embed.add_field(name="Links", value=issue_links, inline=False)
        embed.add_field(name="Reporter", value=f"{self.user.name}#{self.user.discriminator}", inline=False)
        embed.add_field(name="Issue URL", value=url, inline=False)
        await interaction.response.send_message(embeds=[embed])


class LabelView(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @ui.select(
        placeholder="Choose a report label",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(
                label="Bug",
                description="Issues relating to code behavior"
            ),
            SelectOption(
                label="Gameplay",
                description="Issues with gameplay"
            ),
            SelectOption(
                label="Visual",
                description="Visual issues that do not have any impact on gameplay"
            ),
            SelectOption(
                label="Accessibility",
                description="Issues that cause accessibility concerns"
            ),
            SelectOption(
                label="Other",
                description="Any issue that doesn't fit in any other label"
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        label = select.values[0]
        user = interaction.user
        await interaction.response.send_modal(ReportModal(label, user, title=f"{label} Issue Report"))
        await self.message.delete()

    async def on_timeout(self) -> None:
        await self.message.delete()
