import pytest
from unittest.mock import patch
from stacksorbit_gui import StacksOrbitGUI
from textual.widgets import DataTable
from textual.widgets.data_table import RowKey

@pytest.mark.asyncio
async def test_contract_categorization():
    """Test that contracts are correctly categorized based on their name."""
    app = StacksOrbitGUI()

    # DEX (should match first)
    assert app._categorize_contract("token-swap") == "dex"

    # Base
    assert app._categorize_contract("sip-010-trait") == "base"
    assert app._categorize_contract("math-utils") == "base"

    # Tokens
    assert app._categorize_contract("my-token") == "tokens"
    assert app._categorize_contract("sip-010-token") == "tokens"

    # NFT
    assert app._categorize_contract("cool-nft") == "nft"

    # Oracle
    assert app._categorize_contract("price-feed") == "oracle"

    # Governance
    assert app._categorize_contract("dao-proposal") == "governance"

    # Security
    assert app._categorize_contract("access-control") == "security"

    # Monitoring
    assert app._categorize_contract("project-registry") == "monitoring"

    # Other
    assert app._categorize_contract("random-contract") == "other"

@pytest.mark.asyncio
async def test_contract_details_header_with_category():
    """Verify that the Contract Details header includes categorization info."""
    app = StacksOrbitGUI()
    async with app.run_test() as pilot:
        contracts_table = app.query_one("#contracts-table")
        header_label = app.query_one("#contract-details-header-label")

        # Add a token contract
        contracts_table.add_row("🪙", "my-token", "ST123", key="ST123.my-token")
        await pilot.pause()

        # Simulate highlight
        app.on_contracts_row_highlighted(
            DataTable.RowHighlighted(
                data_table=contracts_table,
                row_key=RowKey("ST123.my-token"),
                cursor_row=0
            )
        )
        await pilot.pause()

        # Check header label (🪙 Token)
        render_output = str(header_label.render())
        assert "my-token" in render_output
        assert "🪙 Token" in render_output
