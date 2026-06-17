import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from stacksorbit_gui import StacksOrbitGUI
from textual.widgets import DataTable

# Mock data
mock_contracts = [{"contract_id": "ST123.test"}]
mock_transactions = [
    {
        "tx_id": "0x123",
        "tx_type": "smart_contract",
        "tx_status": "success",
        "block_height": 100,
    }
]
mock_api_status = {"status": "online", "block_height": 500}
mock_account_info = {"balance": "1000000", "nonce": 1}
mock_runway = {"runway_months": 12}
mock_exit_velocity = {"current_estimated_valuation_zar": 500000}


@pytest.mark.asyncio
async def test_update_data_skips_clear_when_data_is_same():
    """Verify that update_data does not clear tables if data has not changed."""
    with patch("stacksorbit_gui.asyncio.gather", new_callable=AsyncMock) as mock_gather:
        mock_gather.return_value = (
            mock_runway,
            mock_exit_velocity,
            mock_api_status,
            mock_account_info,
            mock_contracts,
            mock_transactions,
        )

        app = StacksOrbitGUI()
        app.address = "ST123..."
        app._last_contracts = mock_contracts
        app._last_transactions = mock_transactions
        app._all_transactions = mock_transactions
        app.current_block_height = 500
        app._last_height = 500

        async with app.run_test() as pilot:
            # Re-verify and stabilize state after mount
            app.current_block_height = 500
            app._last_height = 500
            app._last_contracts = mock_contracts
            app._all_transactions = mock_transactions

            # Populate metrics to avoid status/height updates
            app._last_metrics = {
                "status": "[green]●[/] ONLINE",
                "height": "500",
                "runway": "12 mo",
                "balance": "[green]1.000000 STX[/]",
                "nonce": "1",
                "contract-count": "1",
            }

            with patch.object(DataTable, "clear") as mock_clear:
                await app.update_data()
                mock_clear.assert_not_called()


@pytest.mark.asyncio
async def test_update_data_calls_clear_when_data_changes():
    """Verify that update_data clears tables if data has changed."""
    with patch("stacksorbit_gui.asyncio.gather", new_callable=AsyncMock) as mock_gather:
        mock_gather.return_value = (
            mock_runway,
            mock_exit_velocity,
            mock_api_status,
            mock_account_info,
            mock_contracts,
            mock_transactions,
        )

        app = StacksOrbitGUI()
        app.address = "ST123..."
        app._last_contracts = []
        app._last_transactions = []

        with patch.object(app, "run_worker") as mock_run_worker:
            async with app.run_test() as pilot:
                app._last_contracts = []
                app._all_transactions = []
                app._last_height = 0

                with patch.object(DataTable, "clear") as mock_clear:
                    await app.update_data()
                # Should be called twice: once for contracts, once for transactions
                assert mock_clear.call_count == 2
