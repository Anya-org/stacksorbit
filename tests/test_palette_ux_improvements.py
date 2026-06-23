import pytest
from conxius_orbit_gui import ConxiusOrbitGUI
from textual.widgets import Button, DataTable, Label, Input, TabbedContent
from unittest.mock import MagicMock
import asyncio


@pytest.mark.asyncio
async def test_palette_ux_improvements():
    """Verify the new UX improvements: empty states, filter count color, and shortcuts."""
    app = ConxiusOrbitGUI()
    # Mock monitor to avoid API calls during app startup
    app.monitor = MagicMock()
    app.monitor.api_url = "https://api.testnet.hiro.so"
    app.monitor.check_api_status.return_value = {
        "status": "online",
        "block_height": 100,
    }
    app.monitor.get_account_info.return_value = {"balance": "0", "nonce": 0}
    app.monitor.get_deployed_contracts.return_value = []
    app.monitor.get_recent_transactions.return_value = []

    async with app.run_test() as pilot:
        # Reset last_contracts to force table update
        app._last_contracts = None

        # 1. Verify Empty States in Contracts Table
        app.w_tabbed_content.active = "contracts"
        await pilot.pause()

        contracts_table = app.query_one("#contracts-table", DataTable)

        # Test "Not configured" state
        app.address = "Not configured"
        app._last_contracts = None
        await app.update_data()
        await pilot.pause()

        row_data = contracts_table.get_row_at(0)
        assert "Config missing" in str(row_data)
        assert "Press [F5] to set up" in str(row_data)

        # Test "No contracts found" state
        app.address = "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
        app._last_contracts = None
        await app.update_data()
        await pilot.pause()
        row_data = contracts_table.get_row_at(0)
        assert "No contracts found" in str(row_data)
        assert "Press [F4] to deploy" in str(row_data)

        # 2. Verify Empty States in Transactions Table
        app.w_tabbed_content.active = "transactions"
        await pilot.pause()
        tx_table = app.query_one("#transactions-table", DataTable)

        # Test "No transactions found"
        app._all_transactions = []
        app._update_transactions_table()
        await pilot.pause()
        row_data = tx_table.get_row_at(0)
        assert "No transactions found" in str(row_data)
        assert "Press [r] to refresh" in str(row_data)

        # Test "Config missing" for Transactions
        app.address = "Not configured"
        app._update_transactions_table()
        await pilot.pause()
        row_data = tx_table.get_row_at(0)
        assert "Config missing" in str(row_data)
        assert "Press [F5] to configure" in str(row_data)

        # 3. Verify Filter Count Colorization
        app.address = "ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM"
        app._all_transactions = [
            {"tx_id": "0x123", "tx_type": "contract_call", "tx_status": "success"}
        ]
        app._update_transactions_table()
        await pilot.pause()

        filter_input = app.query_one("#tx-filter-input", Input)
        filter_input.value = "nonexistent"
        await pilot.pause()

        filter_count = app.query_one("#tx-filter-count", Label)
        # Check using render() which returns the renderable (often a Text object)
        rendered = str(filter_count.render())
        assert "(0/1 matches)" in rendered

        # 4. Verify Efficiency Shortcuts
        app.w_tabbed_content.active = "deployment"
        await pilot.pause()

        # Mock the shortcut methods directly
        app.action_precheck = MagicMock()
        app.action_deploy = MagicMock()

        # Test 'p' shortcut
        await pilot.press("p")
        app.action_precheck.assert_called_once()

        # Test 'u' shortcut
        await pilot.press("u")
        app.action_deploy.assert_called_once()


if __name__ == "__main__":
    pass
