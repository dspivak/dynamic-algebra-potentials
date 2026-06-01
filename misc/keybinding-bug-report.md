# `up:null` / `down:null` in keybindings.json does not suppress history recall (arrows still scroll history)

## Summary
Setting the Up/Down arrows to `null` in `~/.claude/keybindings.json` (to stop history navigation in the prompt) has **no effect**: pressing Up still recalls the previous prompt from history. The override is loaded successfully (the debug log confirms `Loaded 2 user bindings`), but the arrow→history behavior is not suppressed. Per the docs, setting a key to `null` should unbind it.

## Environment
- Claude Code **2.1.157**
- Platform: macOS (darwin 24.2.0), zsh, iTerm2
- Binary: `~/.local/share/claude/versions/2.1.157`

## `~/.claude/keybindings.json`
```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    { "context": "Chat", "bindings": { "up": null, "down": null } }
  ]
}
```

## Steps to reproduce
1. Put the file above at `~/.claude/keybindings.json`.
2. Launch Claude Code so the file is actually read (see note on the gate below). Confirm via `--debug`: the log shows
   `[keybindings] Loaded 2 user bindings from ~/.claude/keybindings.json`
   and `KeybindingSetup initialized with 175 bindings, 0 warnings`.
3. At the prompt, type some text (e.g. `hello`).
4. Press the **Up** arrow.

## Expected
With `up` unbound (`null`) in the `Chat` context, pressing Up should **not** trigger `history:previous`. (Ideally the input's native cursor movement remains.)

## Actual
Pressing Up still triggers history recall — the typed text is replaced by the previous prompt from history. `down:null` likewise does not suppress `history:next`.

## Evidence it's loaded but ineffective
- Debug log: `[keybindings] Loaded 2 user bindings ... initialized with 175 bindings, 0 warnings` (no parse/validation errors).
- Default bindings in the binary: `up:"history:previous"`, `down:"history:next"`, defined **only** in the `Chat` context — which is exactly the context being overridden.
- Verified behaviorally by injecting a real Up keypress (`\x1b[A`) into an interactive session via a pty: typed a unique marker, pressed Up, and the marker was replaced by a recalled history entry — with the `null` override fully loaded.

## Notes / possibly related
- There is no bindable "move cursor up/down a line" action (only `chat:*`, `history:*`, `scroll:*`, etc.), and no settings key to disable arrow-history. So users currently have no working way to stop the arrows from recalling history.
- Rebinding the arrows to other actions (`app:redraw`, `scroll:lineUp`, `chat:clearInput`) also did not reliably suppress history, which suggests the arrow→history behavior may be handled inside the input component **below** the keybinding-dispatch layer, rather than via the `history:previous`/`history:next` bindings.
- Separately (not the bug, but it made this hard to diagnose): on this account the keybinding feature gate (`tengu_keybinding_customization_release`) is OFF, so `keybindings.json` is silently ignored entirely unless launched with `DISABLE_GROWTHBOOK=1` in the **process** environment. The `env` block in `settings.json` does *not* satisfy this (it only injects into child/tool processes, not Claude's own `process.env`).

## Requested fix
Make `null` actually unbind Up/Down in the `Chat` context (suppress `history:previous`/`history:next`), and/or expose a setting or bindable action to disable history-on-arrow while keeping native multi-line cursor movement.
