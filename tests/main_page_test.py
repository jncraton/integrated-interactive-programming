"""
Tests for the teacher view of the application

These are the end-to-end UI test for index.html
"""

import re
from playwright.sync_api import Page, expect, Error
import pytest


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """Load the page before each test"""
    page.goto("http://localhost:8000")


def test_desired_outcome(page: Page):
    """Confirm that output text is visible"""

    textbox_locator = page.locator("#target-text")
    assert textbox_locator.is_visible()


def test_student_link_navigates(page: Page):
    """Confirm that student link copies correctly"""

    # Step 1: Input text in input field
    page.locator("#code-area").fill("test input")

    # Step 2: Input text in output field
    page.locator("#target-text").fill("test output")

    # Step 3: Copy Link
    try:
        # Acquire clipboard-write. This is only supported and required in Chromium.
        page.context.grant_permissions(["clipboard-write"])
    except Error:
        pass

    page.locator("#copy").click()

    expect(page.locator("#copy")).to_contain_text("Copied")


def test_initial_share_url(page: Page):
    """Confirm that the sharing url is populated on page load"""

    expect(page.locator("#share-text")).to_have_value(re.compile(r"http.*"))


def test_embed_code_generation(page: Page):
    """Confirm that the embed link returns the expected URL"""

    page.locator("#code-area").fill("Sample code")
    page.locator("#target-text").fill("Sample output")
    page.locator("#class-code").fill("CLS1")
    page.locator("#assignment-code").fill("Assignment1")

    # Select embed mode
    page.select_option("select#share-type", label="Embed")

    # Generate the expected URL based on the inputs
    expected_url = page.evaluate(
        """location.origin + location.pathname + "exercise#" + 
        btoa(JSON.stringify(["Sample code", "Sample output", 
        "CLS1", "Assignment1"])) """
    )
    # Construct the expected embed code
    expected_embed_code = (
        f'<iframe src="{expected_url}" width="100%" '
        f'height="800" frameborder="0" allowfullscreen></iframe>'
    )

    # Assert that the displayed embed code matches the expected embed code
    expect(page.locator("#share-text")).to_have_value(expected_embed_code)
