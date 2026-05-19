## 2025-03-08 - [Dashboard Metric Accessibility]
**Learning:** Custom 'metric card' containers in Textual (using `Container` or `Grid`) are not focusable by default. To make them keyboard-accessible, `can_focus = True` must be set explicitly in `on_mount`, and an `on_key` handler must be implemented to map 'enter' to their respective click actions. This ensures users with screen readers or keyboard-only setups can navigate and interact with dashboard summaries.
**Action:** Always audit custom UI components for focusability and provide `on_key` handlers for primary interactions (Enter/Space).

## 2025-03-08 - [Enhanced Copy Feedback]
**Learning:** While button-label changes (📋 -> ✅) provide some feedback, users often look at the data they are copying. Providing feedback directly on the label containing the data (e.g., "Copied to clipboard!") provides more immediate and contextual confirmation of the action.
**Action:** Use a temporary label update pattern alongside button changes for high-intent copy actions.

## 2025-03-09 - [Actionable Empty States]
**Learning:** Empty states in data tables often contain instructions (e.g., "Press [F4] to deploy"). Making these placeholder rows interactive by assigning unique keys and handling `RowSelected` events provides a delightful "shortcut" that aligns with the user's intent, improving accessibility for keyboard and mouse users alike.
**Action:** Use unique row keys for placeholder rows to enable contextual navigation or actions directly from the table.

## 2025-03-23 - [Interactive Validation Feedback]
**Learning:** Providing immediate visual confirmation (e.g., green border and checkmark) for valid inputs in addition to error feedback significantly improves the user's confidence and clarity during data entry.
**Action:** Implement positive validation states (`.success`) for critical input fields to balance error-only feedback.

## 2025-03-23 - [Reactive State-Aware Buttons]
**Learning:** When a button action (like "Save") triggers a temporary state change ("Saved!"), restoring the button's appearance based on the current *reactive* state of the application is more robust than blindly restoring its *previous* label, especially if other UI events occurred during the action.
**Action:** Use application reactive state (e.g., `self.unsaved_changes`) to derive UI button labels and variants after asynchronous operations.

## 2025-03-24 - [Visual Categorization via Icons]
**Learning:** In data-dense tables (like contract lists), replacing generic checkmarks with high-fidelity icons (emojis) based on content heuristics significantly improves scannability and user delight. It allows users to quickly differentiate between contract types (e.g., Tokens vs DEX) at a glance.
**Action:** Implement heuristic-based categorization for list-based data and use specific visual indicators (icons) to represent the underlying purpose or type.

## 2025-04-02 - [Reactive Theme Switching]
**Learning:** In Textual, themes can be implemented reactively by defining a `theme_name` reactive variable and using a `watch_theme_name` method to dynamically swap CSS classes on the `App` instance. This allows for instant visual feedback without requiring an application restart. For global overrides like background and text color, CSS rules should specifically target the `Screen` widget.
**Action:** Use reactive properties and CSS class swapping on the `App` instance for seamless, live UI customization.

## 2025-05-15 - [Multi-Channel Feedback for Copy Actions]
**Learning:** For high-value copy actions (like wallet addresses), providing feedback on both the trigger (button icon change) and the target data label (temporary "Copied!" text) ensures the user notices the success even if their focus is split. This is especially important in high-density dashboards where small icon changes might be missed.
**Action:** Implement dual-channel feedback (button + label) for critical copy operations.

## 2025-06-12 - [Context-Aware Data Extraction]
**Learning:** In a data-heavy dashboard, users frequently need to extract specific values. Implementing context-aware copy logic that detects focused 'metric cards' and provides clean, text-only copies (via OSC 52 for terminal compatibility) significantly reduces user friction compared to manual selection. Explicitly cleaning UI markup from the copied string is essential for a professional experience.
**Action:** Map the universal copy shortcut [c] to a context-aware dispatcher that intelligently handles focused data widgets and provides descriptive notifications.
