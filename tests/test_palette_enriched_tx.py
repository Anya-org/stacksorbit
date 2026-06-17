import pytest
from unittest.mock import MagicMock
from stacksorbit_gui import StacksOrbitGUI
from textual.widgets import DataTable
from textual.widgets.data_table import RowKey


@pytest.mark.asyncio
async def test_enriched_transaction_details():
    """Verify that highlighting a transaction displays enriched details in the action bar."""
    app = StacksOrbitGUI()
    # Mock monitor to avoid API calls
    app.monitor = MagicMock()

    async with app.run_test() as pilot:
        # Mock transaction data
        tx_id = "0x1234567890abcdef1234567890abcdef12345678"

        # Switch to transactions tab to ensure widgets are mounted
        await pilot.press("f3")
        await pilot.pause()

        # POPULATE AFTER STARTUP
        app._all_transactions = [
            {
                "tx_id": tx_id,
                "tx_type": "contract_call",
                "tx_status": "success",
                "nonce": 42,
                "fee_rate": "1500",
                "block_height": 100,
            }
        ]

        tx_table = app.query_one("#transactions-table", DataTable)
        status_label = app.query_one("#tx-status-label")

        # Add row to table
        tx_table.add_row("0x1234...", "call", "success", "1m ago", "100", key=tx_id)
        await pilot.pause()

        # Simulate row highlighting
        app.on_transactions_row_highlighted(
            DataTable.RowHighlighted(
                data_table=tx_table, row_key=RowKey(tx_id), cursor_row=0
            )
        )
        await pilot.pause()

        # Verify label content
        rendered_text = str(status_label.render())
        # Check for truncated ID (first 16 chars as per implementation)
        assert "0x1234567890abcd" in rendered_text
        assert "contract call" in rendered_text
        assert "Nonce: 42" in rendered_text
        assert "Fee: 1500" in rendered_text


@pytest.mark.asyncio
async def test_enriched_transaction_details_empty_state():
    """Verify that highlighting an empty state row handles it gracefully."""
    app = StacksOrbitGUI()
    app.monitor = MagicMock()

    async with app.run_test() as pilot:
        await pilot.press("f3")
        await pilot.pause()

        tx_table = app.query_one("#transactions-table", DataTable)
        status_label = app.query_one("#tx-status-label")

        # Simulate an "empty-refresh" row highlighting (e.g. "No transactions found")
        app.on_transactions_row_highlighted(
            DataTable.RowHighlighted(
                data_table=tx_table, row_key=RowKey("empty-refresh"), cursor_row=0
            )
        )
        await pilot.pause()

        # Verify it shows the default message and buttons are disabled
        assert "Select a transaction to see actions" in str(status_label.render())
        assert app.query_one("#copy-selected-tx-btn").disabled is True
        assert app.query_one("#view-selected-tx-explorer-btn").disabled is True
