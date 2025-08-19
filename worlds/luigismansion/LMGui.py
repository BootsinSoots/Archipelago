from kvui import GameManager, MDLabel, MDBoxLayout, MDDivider

def build_gui(ui: GameManager):
    ui.lm_layout = MDBoxLayout(orientation="vertical")
    divider = MDDivider()
    ui.wallet_ui = MDLabel(text="Wallet:0/0", halign="center", font_style="Display")
    ui.boo_count = MDLabel(text="Boo Count: 0", halign="center", font_style="Display")

    ui.lm_layout.add_widget(ui.boo_count)
    ui.lm_layout.add_widget(divider)
    ui.lm_layout.add_widget(ui.wallet_ui)

    ui.add_client_tab("Luigi's Mansion", ui.lm_layout)

