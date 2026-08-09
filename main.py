import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogButtonContainer,
)

class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.qizlar_bazasi = [
            "Aysun", "Ayan", "Zərifə", "Hüsniyyə", "Ləman", "Südabə", "Nazlı", "Nəzrin", "Səma",
            "Gülər", "Leyla", "Nərgiz", "Nigar", "Günel", "Fidan", "Xədicə", "Zəhra", "Məryəm",
            "Səbinə", "Aytən", "Elya", "Aynur", "Dəniz", "Nərmin", "Arzu", "Lalə", "Sevda"
        ]
        
        self.oglanlar_bazasi = [
            "İsa", "Tunar", "İbrahim", "Sənan", "Yusif", "Rəsul", "Həmid", "Ramal", "Rəvan",
            "Murad", "Əli", "Hüseyn", "Tural", "Elvin", "Kənan", "Orxan", "Anar", "Vüqar",
            "Nihad", "Rauf", "Zaur", "Cavid", "Fərid", "Elnur", "Kamran", "Emin", "Rəşad"
        ]

        self.ceteler = ["FQ Məkanı", "Mayhem", "Baku Boys", "Azelow", "Yetim"]
        self.cinsiyyet = "Kişi"
        self.dialog = None

        self.main_game_box = MDBoxLayout(orientation='vertical')

        self.top_bar = MDBoxLayout(orientation='horizontal', size_hint_y=None, height="50dp", padding=[15, 5, 15, 5])
        self.stats_right_label = MDLabel(text="", halign="right", theme_text_color="Custom", text_color=[0.2, 0.7, 0.3, 1])
        self.top_bar.add_widget(self.stats_right_label)
        self.main_game_box.add_widget(self.top_bar)

        self.game_scroll = MDScrollView()
        self.game_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=None)
        self.game_layout.bind(minimum_height=self.game_layout.setter('height'))

        self.info_label = MDLabel(text="", halign="center")
        self.game_layout.add_widget(self.info_label)

        self.buttons_layout = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.buttons_layout.bind(minimum_height=self.buttons_layout.setter('height'))
        self.game_layout.add_widget(self.buttons_layout)

        self.game_scroll.add_widget(self.game_layout)
        self.main_game_box.add_widget(self.game_scroll)

        self.setup_menu()

    def setup_menu(self):
        if self.main_game_box in self.children:
            self.remove_widget(self.main_game_box)

        self.menu_layout = MDBoxLayout(orientation='vertical', padding=30, spacing=15, pos_hint={"center_x": 0.5, "center_y": 0.5})
        
        # Pəncərənin başlıq hissəsini (Window title) dəyişmək üçün MDApp-a müraciət edirik
        MDApp.get_running_app().title = "AZE SİMULASYONU"

        title = MDLabel(text="🇦🇿 AZE SİMULASYONU", halign="center", font_style="Display", role="small")
        self.menu_layout.add_widget(title)

        self.gender_label = MDLabel(text=f"Seçilmiş Cinsiyyət: {self.cinsiyyet}", halign="center")
        self.menu_layout.add_widget(self.gender_label)

        gender_box = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height="40dp")
        btn_kisi = MDButton(size_hint=(0.5, 1), on_release=lambda x: self.cinsiyyet_deyis("Kişi"))
        btn_kisi.add_widget(MDButtonText(text="👨 Kişi"))
        
        btn_qadin = MDButton(size_hint=(0.5, 1), on_release=lambda x: self.cinsiyyet_deyis("Qadın"))
        btn_qadin.add_widget(MDButtonText(text="👩 Qadın"))
        
        gender_box.add_widget(btn_kisi)
        gender_box.add_widget(btn_qadin)
        self.menu_layout.add_widget(gender_box)

        self.name_input = MDTextField(hint_text="Xarakterin Adı", mode="outlined")
        self.surname_input = MDTextField(hint_text="Xarakterin Soyadı", mode="outlined")
        self.menu_layout.add_widget(self.name_input)
        self.menu_layout.add_widget(self.surname_input)

        start_btn = MDButton(size_hint=(1, None), on_release=self.oyunu_baslat)
        start_btn.add_widget(MDButtonText(text="🚀 OYUNA BAŞLA"))
        self.menu_layout.add_widget(start_btn)

        self.add_widget(self.menu_layout)

    def cinsiyyet_deyis(self, secim):
        self.cinsiyyet = secim
        self.gender_label.text = f"Seçilmiş Cinsiyyət: {self.cinsiyyet}"

    def yarasigliq_metni(self):
        if self.yarasigliq_xal < 30: return "Çox Çirkin"
        elif self.yarasigliq_xal < 50: return "Çirkin"
        elif self.yarasigliq_xal < 70: return "Adi"
        elif self.yarasigliq_xal < 90: return "Gözəl / Yaraşıqlı"
        else: return "Model Kimi"

    def bildiris_goster(self, metn):
        if self.dialog:
            try:
                self.dialog.dismiss()
            except:
                pass
            self.dialog = None
        ok_btn = MDButton(on_release=lambda x: self.dialog.dismiss())
        ok_btn.add_widget(MDButtonText(text="Aydındır"))
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=metn),
            MDDialogButtonContainer(ok_btn)
        )
        self.dialog.open()

    def add_btn(self, text, callback):
        btn = MDButton(size_hint=(1, None), on_release=callback)
        btn.add_widget(MDButtonText(text=text))
        self.buttons_layout.add_widget(btn)

    def oyunu_baslat(self, instance):
        default_ad = "İbrahim" if self.cinsiyyet == "Kişi" else "Aysun"
        self.ad = self.name_input.text.strip().capitalize() if self.name_input.text.strip() else default_ad
        self.soyad = self.surname_input.text.strip().capitalize() if self.surname_input.text.strip() else "Məmmədov"
        
        self.yash = 1
        self.can = 100
        self.xosbextlik = 100
        self.guc = 20
        self.agil = 0
        self.yarasigliq_xal = 10
        self.pul = 0
        self.populerlik = 20
        self.sevgili = "Yoxdur"
        self.evli = False
        self.cete = "Yoxdur"
        self.son_cete_savas_yasi = -10
        self.is_unvani = "Uşaq"
        self.maas = 0
        self.ali_tehsil = False
        self.esgerlik_olunub = False
        self.xestelik = "Sağlam"
        
        self.masinlar = []
        self.evler = []
        
        self.ogurluq_sayi = 0
        self.meth = 0
        self.pive = 0
        self.silah_sayi = 0
        self.bicag_sayi = 0
        self.sigaret = 0
        self.hebsxanadadir = False
        self.ceza_muddeti = 0
        self.olum_sebebi = "Təbii qocalıq"

        self.generate_rich_ssenarileri()

        if self.menu_layout in self.children:
            self.remove_widget(self.menu_layout)
        if self.main_game_box not in self.children:
            self.add_widget(self.main_game_box)
        
        self.bildiris_goster(f"👶 {self.ad} {self.soyad} ({self.cinsiyyet}) olaraq 0 AZN ilə dünyaya gəldin!")
        self.refresh_buttons()
        self.update_stats()

    def generate_rich_ssenarileri(self):
        self.mekteb_ssenarileri = [
            {
                "sual": "🏫 Riyaziyyat imtahanında sinfin ən ağıllı şagirdi cavabları sənə göstərir. Nə edirsən?",
                "secim1": ("Köçürüb əla qiymət al", 0, -5, 0, 0, 5, 10, "İmtahandan 5 aldın, amma heç nə öyrənmədin."),
                "secim2": ("Vicdanına qulaq asıb özün yaz", 0, 5, 0, 0, -5, 5, "Zəif qiymət aldın, amma vicdanın rahatdır."),
                "secim3": ("Müəllimə xəbər ver ki, o köçürür", 0, 0, -5, 0, -20, -10, "Sinif yoldaşların səni boykot etdi.")
            },
            {
                "sual": "🎒 Məktəb həyətində böyük sinif şagirdləri səndən pul tələb edir.",
                "secim1": ("Cibində pul yoxdur deyə qurtardın", 0, 0, 0, 0, 0, -5, "Pulun olmadığı üçün səndən heç nə ala bilmədilər."),
                "secim2": ("Etiraz edib dava sal", -15, 0, 10, 0, 10, -5, "Qəhrəmanca vuruşdun, amma bədənin zədələndi."),
                "secim3": ("Qaçıb məktəb direktoruna şikayət et", 0, 0, -5, 0, -5, 5, "Problemi həll etdin, amma səni 'qorxaq' adlandırdılar.")
            }
        ]
        self.boyuk_ssenarileri = [
            {
                "sual": "💼 Gecə saat 3-də işlədiyin şirkətin serverləri çöktü və rəhbər səni təcili işə çağırır.",
                "secim1": ("Dərhal taksiyə minib problemi həll et", 0, 5, 0, -20, 15, 10, "Rəhbərlik fədakarlığını qiymətləndirib mükafat verdi!"),
                "secim2": ("Telefonun səsini alıb yatmağa davam et", 0, 0, 0, 0, -10, 10, "Səhər işdə şiddətli danlaq eşitdin."),
                "secim3": ("Bəhanə gətirib gəlmədiyini de", 0, 0, 0, 0, -5, 5, "İşdə mövqeyin zəiflədi.")
            }
        ]
        self.qoca_ssenarileri = [
            {
                "sual": "👴 Nəvələrin evə qaçıb gəlib sizdən bazarçılıq üçün pul və ya hədiyyə istəyirlər.",
                "secim1": ("Cibindən pul ver", 0, 0, 0, -20, 15, 30, "Nəvələrin səni qucaqlayıb öpdü."),
                "secim2": ("'Pulcum yoxdur' de", 0, 5, 0, 0, 2, -10, "Uşaqlar qorxub kənara çəkildi."),
                "secim3": ("Nərd oynamağa dəvət et", 0, 0, 0, 0, 5, 15, "Nəvə ilə gözəl zaman keçirdiniz.")
            }
        ]

    def update_stats(self):
        depressiya_str = " | ⚠️ DEPRESSİYA!" if self.xosbextlik <= 20 else ""
        self.stats_right_label.text = (
            f"😊 Xoşbəxtlik: {self.xosbextlik}%  |  🧠 Ağıl: {self.agil}%  |  🎂 Yaş: {self.yash}  |  ❤️ Can: {self.can}%  |  ✨ Görünüş: {self.yarasigliq_metni()}  |  💵 {self.pul} AZN{depressiya_str}"
        )

        if self.can <= 0:
            self.info_label.text = (
                f"☠️ OYUN BİTDİ!\n"
                f"👤 {self.ad} {self.soyad} {self.yash} yaşında vəfat etdi.\n\n"
                f"⚰️ Əcəl Səbəbi: {self.olum_sebebi}"
            )
            self.refresh_buttons()
            return

        if self.hebsxanadadir:
            self.info_label.text = f"🔒 HƏBSXANadAniz 🔒\n⚖️ Cəza: {self.ceza_muddeti} İL"
        else:
            masin_str = ", ".join(self.masinlar) if self.masinlar else "Yoxdur"
            ev_str = ", ".join(self.evler) if self.evler else "Yoxdur"
            evlilik_durum = f"Evli (Həyat yoldaşı: {self.sevgili}) 💍" if self.evli else f"Sevgili: {self.sevgili}"
            
            self.info_label.text = (
                f"👤 {self.ad} {self.soyad} ({self.cinsiyyet}) | 🏢 İş: {self.is_unvani}\n"
                f"🏋️ Güc: {self.guc}% | ⭐ Populyarlıq: {self.populerlik}%\n"
                f"🤒 Sağlamlıq: {self.xestelik} | 🎓 Ali Təhsil: {'Var' if self.ali_tehsil else 'Yoxdur'}\n"
                f"🪖 Əsgərlik: {'Keçib' if self.esgerlik_olunub else 'Keçməyib'} | 🔫 Silah: {self.silah_sayi} | 🔪 Bıçaq: {self.bicag_sayi}\n"
                f"👥 Çətə: {self.cete} | 💕 {evlilik_durum}\n"
                f"🚗 Maşın: {masin_str} | 🏠 Mülk: {ev_str}"
            )

    def refresh_buttons(self):
        self.buttons_layout.clear_widgets()
        if self.can <= 0:
            self.add_btn("🔄 YENİDƏN BAŞLA (ANA MENYU)", lambda x: self.setup_menu())
            return

        self.add_btn("📅 --- 1 İL YAŞLAN ---", self.yaslan)

        if self.yash < 6:
            return

        if self.hebsxanadadir:
            self.add_btn("🏃 HƏBSXANadAn QAÇMAĞA CƏHD ET", self.hebsden_qac)
        else:
            self.add_btn("📖 Kitab Oxu / Dərs Çalış (+Ağıl)", self.ders_oxu)
            if self.yash >= 17 and not self.ali_tehsil:
                self.add_btn("🎓 Universitetə Müraciət Et", self.universitet_müraciet)
            self.add_btn("💼 Karyera və İş Bazarı", self.karyera_menusu)
            self.add_btn("🚗 Auto & Mülk Marketi (Maşın/Ev)", self.mulk_marketi)
            if self.masinlar:
                self.add_btn("🏎️ Maşın Sür (Səyahət / Yarış)", self.masin_sur_menusu)
            self.add_btn("🏥 Xəstəxanaya Get (Müalicə Ol)", self.xestexana)
            self.add_btn("🍵 Çayxana / Kino / Klub (Xoşbəxtlik artır)", self.eylence_menusu)
            
            if self.sevgili == "Yoxdur":
                sevgili_metn = "❤️ Qızlara Təklif Et" if self.cinsiyyet == "Kişi" else "❤️ Oğlanlara Təklif Et"
                self.add_btn(sevgili_metn, self.sevgili_menusu)
            elif not self.evli:
                self.add_btn("💔 Sevgilidən Ayrıl", self.sevgiliden_ayril)
                if self.yash >= 18:
                    self.add_btn("💍 Evlilik Təklifi Et", self.evlilik_teklifi_et)
                    self.add_btn("🍼 Körpə Planlaşdır (Hamilə Qoy)", self.korpe_planlasdir)
            else:
                self.add_btn("📜 Boşan", self.sevgiliden_ayril)
                self.add_btn("🍼 Körpə Planlaşdır (Hamilə Qoy)", self.korpe_planlasdir)

            self.add_btn("💈 Bərbər və İdman Zalı (400 AZN)", self.yarasigliq_artir)
            self.add_btn("🛒 Marketdən Oğurluq Et", self.ogurluq_et)
            self.add_btn("🎒 İnventardakı Malları Sat", self.mal_sat)
            self.add_btn("👊 Dava Etmək Üçün Adam Seç", self.dava_menusu)
            self.add_btn("💣 Qara Bazar (Silah/Meth/Bıçaq)", self.qara_bazar_menusu)
            self.add_btn("🔪 Çətə Seç və Qoşul", self.cete_secim_menusu)
            if self.cete != "Yoxdur":
                self.add_btn("⚔️ Çətə Savaşı Başlat (Uğurlu olarsa pul gələr)", self.cete_savas_menusu)

    def yaslan(self, instance):
        if self.can <= 0: return
        self.yash += 1
        self.ogurluq_sayi = 0

        if self.maas > 0 and not self.hebsxanadadir:
            self.pul += self.maas

        if self.hebsxanadadir:
            self.ceza_muddeti -= 1
            if self.ceza_muddeti <= 0:
                self.hebsxanadadir = False
                self.bildiris_goster("🔓 Cəza müddətin bitdi! Həbsxanadan azadlığa buraxıldın.")
                self.refresh_buttons()
            self.update_stats()
            return

        if self.yash == 18 and self.cinsiyyet == "Kişi" and not self.esgerlik_olunub:
            self.esgerlik_dialog_goster()
            return

        if self.meth > 0:
            self.can = max(0, self.can - (self.meth * 5))

        self.refresh_buttons()
        self.update_stats()

        if self.yash >= 6 and self.yash % 2 == 0:
            self.soru_dialog_goster()

    def esgerlik_dialog_goster(self):
        def esgere_git():
            if self.dialog: self.dialog.dismiss()
            self.esgerlik_olunub = True
            self.guc = min(100, self.guc + 15)
            self.bildiris_goster("🪖 Əsgərlik xidmətini şərəflə başa vurdun! (+15% Güc)")
            self.update_stats()

        def esgerden_qac():
            if self.dialog: self.dialog.dismiss()
            if random.randint(1, 100) <= 40:
                self.esgerlik_olunub = True
                self.bildiris_goster("🏃 Əsgərlikdən uğurla qaçdın və gizlənməyi bacardın!")
            else:
                self.hebsxanadadir = True
                self.ceza_muddeti = 3
                self.bildiris_goster("🚨 Əsgərlikdən qaçarkən POLİS SƏNİ TUTDU! 3 İLLİK HƏBS!")
                self.refresh_buttons()
            self.update_stats()

        b1 = MDButton(on_release=lambda x: esgere_git())
        b1.add_widget(MDButtonText(text="🪖 Hərbi Xidmətə Get (1 İL)"))
        b2 = MDButton(on_release=lambda x: esgerden_qac())
        b2.add_widget(MDButtonText(text="🏃 Əsgərlikdən Qaç (Tutulma Riski VAR)"))

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="🪖 18 Yaşın Tamam Oldu! Hərbi Çağırış Qəbzi Gəldi:"),
            MDDialogButtonContainer(b1, b2)
        )
        self.dialog.open()

    def cete_secim_menusu(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return

        def qosul(cete_adi):
            if self.dialog: self.dialog.dismiss()
            self.cete = cete_adi
            self.bildiris_goster(f"🔪 Təbriklər! '{cete_adi}' çətəsinə qoşuldun!")
            self.refresh_buttons()
            self.update_stats()

        btn_list = []
        for c in self.ceteler:
            btn = MDButton(on_release=lambda x, c_name=c: qosul(c_name))
            btn.add_widget(MDButtonText(text=f"🗡️ {c}"))
            btn_list.append(btn)

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Hansı Çətəyə Qoşulmaq İstəyirsiniz?"),
            MDDialogButtonContainer(*btn_list)
        )
        self.dialog.open()

    def cete_savas_menusu(self, instance):
        if self.yash - self.son_cete_savas_yasi < 5:
            qalan = 5 - (self.yash - self.son_cete_savas_yasi)
            self.bildiris_goster(f"⏳ Çətə savaşı üçün yenidən qüvvə toplamaq lazımdır! {qalan} il gözləməlisən.")
            return

        dusmanlar = [c for c in self.ceteler if c != self.cete]

        def savas_baslat(dusman_cete):
            if self.dialog: self.dialog.dismiss()
            self.son_cete_savas_yasi = self.yash
            
            silah_bonus = self.silah_sayi * 15 + self.bicag_sayi * 8
            sans = random.randint(1, 100) + (self.guc // 2) + silah_bonus
            if sans < 35:
                self.can = 0
                self.olum_sebebi = f"'{dusman_cete}' çətəsi ilə qanlı savaşda həlak olmaq"
                self.bildiris_goster(f"☠️ QANLI SAVAŞ! '{dusman_cete}' çətəsi ilə savaşda vuruldun və ÖLDÜN!")
            elif sans < 65:
                self.can -= 50
                self.xosbextlik -= 20
                self.bildiris_goster(f"🤕 Savaş çox ağır keçdi! Ağır yaralandın (-50% Can), amma sağ qaldın.")
            else:
                qazanc = random.randint(500, 2000)
                self.pul += qazanc
                self.populerlik = min(100, self.populerlik + 20)
                self.bildiris_goster(f"🏆 QƏLƏBƏ! '{dusman_cete}' çətəsini darmadağın etdiniz! Uğurlu savaş nəticəsində +{qazanc} AZN qazandın!")

            self.update_stats()

        btn_list = []
        for d in dusmanlar:
            btn = MDButton(on_release=lambda x, d_name=d: savas_baslat(d_name))
            btn.add_widget(MDButtonText(text=f"⚔️ {d} Çətəsinə Hücum Et"))
            btn_list.append(btn)

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Hansı Çətə İlə Savaşmaq İstəyirsiniz? (Uğurlu olarsa pul gələr)"),
            MDDialogButtonContainer(*btn_list)
        )
        self.dialog.open()

    def ogurluq_et(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return
        self.ogurluq_sayi += 1

        if self.ogurluq_sayi > 3:
            self.hebsxanadadir = True
            self.ceza_muddeti = 2
            self.ogurluq_sayi = 0
            self.bildiris_goster("🚨 POLİS TUTDU! 3 dəfədən çox oğurluq etdiyin üçün marketin təhlükəsizliyi səni yaxaladı! 2 İLLİK HƏBS!")
            self.refresh_buttons()
            self.update_stats()
            return

        self.sigaret += 1
        self.bildiris_goster(f"🛒 Marketdən mal oğurladın! (Bu ilki oğurluq sayın: {self.ogurluq_sayi}/3)")
        self.update_stats()

    def dava_menusu(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return
        reqib_siyahisi = self.oglanlar_bazasi if self.cinsiyyet == "Kişi" else self.qizlar_bazasi
        
        reqib1_ad = random.choice(reqib_siyahisi)
        reqib1_guc = random.randint(15, 95)
        
        reqib2_ad = random.choice(reqib_siyahisi)
        reqib2_guc = random.randint(15, 95)

        def dava_et(ad, reqib_gucu):
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None

            effective_guc = self.guc + (self.silah_sayi * 20) + (self.bicag_sayi * 10)
            if effective_guc >= reqib_gucu:
                qazanc = random.randint(30, 80)
                self.pul += qazanc
                self.guc = min(100, self.guc + 5)
                self.xosbextlik = min(100, self.xosbextlik + 10)
                self.bildiris_goster(f"👊 HALALDIR! {ad} (Güc: {reqib_gucu}%) döydün! (+{qazanc} AZN qazandın)")
            else:
                 alinan_pul = min(self.pul, 200)
                 self.pul -= alinan_pul
                 self.can = max(0, self.can - 25)
                 self.xosbextlik = max(0, self.xosbextlik - 20)
                 if self.can <= 0:
                     self.olum_sebebi = f"{ad} ilə davada ağır zərbə almaq"
                 self.bildiris_goster(f"🤕 UDUZDUN! {ad} (Güc: {reqib_gucu}%) səni döydü və {alinan_pul} AZN pulunu əlindən aldı!")
            self.update_stats()

        b1 = MDButton(on_release=lambda x: dava_et(reqib1_ad, reqib1_guc))
        b1.add_widget(MDButtonText(text=f"🥊 {reqib1_ad} (Güc: {reqib1_guc}%)"))
        b2 = MDButton(on_release=lambda x: dava_et(reqib2_ad, reqib2_guc))
        b2.add_widget(MDButtonText(text=f"🥊 {reqib2_ad} (Güc: {reqib2_guc}%)"))

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Dava etmək üçün adam seç:"),
            MDDialogButtonContainer(b1, b2)
        )
        self.dialog.open()

    def soru_dialog_goster(self):
        if self.yash < 18:
            secilen = random.choice(self.mekteb_ssenarileri)
        elif self.yash < 60:
            secilen = random.choice(self.boyuk_ssenarileri)
        else:
            secilen = random.choice(self.qoca_ssenarileri)

        def secim_icra(can_t, agil_t, guc_t, pul_t, pop_t, xos_t, mesaj):
            if self.dialog:
                self.dialog.dismiss()
                self.dialog = None
            self.can = max(0, min(100, self.can + can_t))
            self.agil = max(0, min(100, self.agil + agil_t))
            self.guc = max(0, min(100, self.guc + guc_t))
            self.pul = max(0, self.pul + pul_t)
            self.populerlik = max(0, min(100, self.populerlik + pop_t))
            self.xosbextlik = max(0, min(100, self.xosbextlik + xos_t))

            self.bildiris_goster(f"📅 {self.yash} Yaş Hadisəsi: {mesaj}")
            self.update_stats()

        s1 = secilen["secim1"]
        s2 = secilen["secim2"]
        s3 = secilen["secim3"]

        b1 = MDButton(on_release=lambda x: secim_icra(s1[1], s1[2], s1[3], s1[4], s1[5], s1[6], s1[7]))
        b1.add_widget(MDButtonText(text=s1[0]))
        b2 = MDButton(on_release=lambda x: secim_icra(s2[1], s2[2], s2[3], s2[4], s2[5], s2[6], s2[7]))
        b2.add_widget(MDButtonText(text=s2[0]))
        b3 = MDButton(on_release=lambda x: secim_icra(s3[1], s3[2], s3[3], s3[4], s3[5], s3[6], s3[7]))
        b3.add_widget(MDButtonText(text=s3[0]))

        self.dialog = MDDialog(
            MDDialogHeadlineText(text=secilen["sual"]),
            MDDialogButtonContainer(b1, b2, b3)
        )
        self.dialog.open()

    def masin_sur_menusu(self, instance):
        if not self.masinlar: return

        def hara_gedek(yoldas):
            if self.dialog: self.dialog.dismiss()
            
            def surus_icra(yer, suret):
                if self.dialog: self.dialog.dismiss()
                if suret > 150:
                    if random.randint(1, 100) <= 40:
                        self.can -= 40
                        self.xosbextlik = max(0, self.xosbextlik - 30)
                        self.bildiris_goster(f"💥 QƏZA! {suret} km/saat sürətlə {yer} istiqamətində gedərkən qəza etdin! (-40% Can)")
                        self.update_stats()
                        return
                
                self.xosbextlik = min(100, self.xosbextlik + 15)
                self.bildiris_goster(f"🏎️ {yoldas} ilə {yer} istiqamətində {suret} km/saat sürətlə sürdünüz.")
                self.update_stats()

            b1 = MDButton(on_release=lambda x: surus_icra("Şəhər Mərkəzi", 60))
            b1.add_widget(MDButtonText(text="🏙️ Şəhər Turu (60 km/h)"))
            b2 = MDButton(on_release=lambda x: surus_icra("Rayon Yolu", 120))
            b2.add_widget(MDButtonText(text="🛣️ Rayon Yolu (120 km/h)"))
            b3 = MDButton(on_release=lambda x: surus_icra("Yarış Zolağı", 220))
            b3.add_widget(MDButtonText(text="🏁 Yarış Trası (220 km/h)"))

            self.dialog = MDDialog(
                MDDialogHeadlineText(text="Hara və neçə km/saat sürətlə sürürsünüz?"),
                MDDialogButtonContainer(b1, b2, b3)
            )
            self.dialog.open()

        b_tek = MDButton(on_release=lambda x: hara_gedek("Təkbaşına"))
        b_tek.add_widget(MDButtonText(text="👤 Təkbaşına"))
        
        yoldas_str = f"Həyat yoldaşın ({self.sevgili})" if self.evli else (f"Sevgili ({self.sevgili})" if self.sevgili != "Yoxdur" else "Dostun")
        b_dost = MDButton(on_release=lambda x: hara_gedek(yoldas_str))
        b_dost.add_widget(MDButtonText(text=f"👥 {yoldas_str} ilə"))

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Maşında kiminlə gedirsiniz?"),
            MDDialogButtonContainer(b_tek, b_dost)
        )
        self.dialog.open()

    def sevgili_menusu(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return
        if self.yash < 12:
            self.bildiris_goster("❌ Sevgili üçün ən az 12 yaşın olmalıdır.")
            return

        namizedler = self.qizlar_bazasi if self.cinsiyyet == "Kişi" else self.oglanlar_bazasi
        secilmisler = random.sample(namizedler, 4)
        
        btn_list = []
        for shasx in secilmisler:
            gozellik_faiz = random.randint(30, 99)
            btn = MDButton(
                size_hint=(1, None),
                on_release=lambda x, s=shasx, g=gozellik_faiz: self.sevgili_teklif_et(s, g)
            )
            btn.add_widget(MDButtonText(text=f"❤️ {shasx} (Gözəllik/Xarizma: {gozellik_faiz}%)"))
            btn_list.append(btn)

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Kimə sevgili təklifi edirsiniz?"),
            MDDialogButtonContainer(*btn_list)
        )
        self.dialog.open()

    def sevgili_teklif_et(self, ad, gozellik):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

        menim_status = self.yarasigliq_metni()

        qebul_etdi = False
        if gozellik < 50:
            if menim_status in ["Çox Çirkin", "Çirkin"]:
                qebul_etdi = True
        elif 50 <= gozellik < 70:
            if menim_status == "Adi":
                qebul_etdi = True
        else:
            if gozellik > 85 and menim_status not in ["Gözəl / Yaraşıqlı", "Model Kimi"]:
                qebul_etdi = False
            else:
                qebul_etdi = True

        if qebul_etdi:
            self.sevgili = f"{ad}"
            self.evli = False
            self.xosbextlik = min(100, self.xosbextlik + 20)
            self.bildiris_goster(f"💖 {ad} (Gözəllik: {gozellik}%) təklifini qəbul etdi! Xoşbəxtliyin artdı.")
        else:
            self.xosbextlik = max(0, self.xosbextlik - 50)
            self.bildiris_goster(f"💔 {ad} səni rədd etdi! Xoşbəxtliyin 50 azaldı.")

        self.refresh_buttons()
        self.update_stats()

    def sevgiliden_ayril(self, instance):
        self.sevgili = "Yoxdur"
        self.evli = False
        self.xosbextlik = max(0, self.xosbextlik - 35)
        self.bildiris_goster("💔 Münasibətə son qoyuldu. Xoşbəxtliyin kəskin düşdü!")
        self.refresh_buttons()
        self.update_stats()

    def evlilik_teklifi_et(self, instance):
        if self.dialog: self.dialog.dismiss()
        if random.randint(1, 100) <= 60:
            self.evli = True
            self.xosbextlik = min(100, self.xosbextlik + 40)
            self.bildiris_goster(f"💍 TƏBRİKLƏR! {self.sevgili} evlilik təklifini qəbul etdi! Artıq rəsmi olaraq evləndiniz!")
        else:
            self.xosbextlik = max(0, self.xosbextlik - 40)
            self.bildiris_goster(f"💔 {self.sevgili} evlilik təklifini rədd etdi! Xoşbəxtliyin yerlə bir oldu...")
        self.refresh_buttons()
        self.update_stats()

    def korpe_planlasdir(self, instance):
        if self.dialog: self.dialog.dismiss()
        if random.randint(1, 100) <= 50:
            self.xosbextlik = min(100, self.xosbextlik + 30)
            self.bildiris_goster(f"🍼 TƏBRİKLƏR! {self.sevgili} ilə uşağınız dünyaya gəldi!")
        else:
            self.xosbextlik = max(0, self.xosbextlik - 20)
            self.bildiris_goster(f"💔 Təəssüf ki, uşaq planınız baş tutmadı.")
        self.update_stats()

    def yarasigliq_artir(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return
        if self.pul < 400:
            self.bildiris_goster("❌ Bərbər və İdman Zalı üçün ən az 400 AZN pulun olmalıdır!")
            return
        self.pul -= 400
        self.yarasigliq_xal = min(100, self.yarasigliq_xal + 15)
        self.guc = min(100, self.guc + 5)
        self.xosbextlik = min(100, self.xosbextlik + 10)
        self.bildiris_goster("💈 Bərbərdə və İdman Zalında görünüşünü düzəltdin! (-400 AZN, +Görünüş, +Güc)")
        self.update_stats()

    def ders_oxu(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return
        self.agil = min(100, self.agil + 10)
        self.bildiris_goster("📖 Kitab oxuyub dərslərini təkrar etdin. (+10% Ağıl)")
        self.update_stats()

    def universitet_müraciet(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return
        if self.agil >= 50:
            self.ali_tehsil = True
            self.bildiris_goster("🎓 Universitetə qəbul olub uğurla bitirdin!")
        else:
            self.bildiris_goster("❌ Ağıl səviyyən az olduğu üçün universitetə qəbul ola bilmədin.")
        self.refresh_buttons()
        self.update_stats()

    def karyera_menusu(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return
        if self.yash < 18:
            self.bildiris_goster("❌ İşləmək üçün yaşı azsan.")
            return

        def ise_gir(unvan, maas_miqdari):
            if unvan == "Proqramçı" and not self.ali_tehsil:
                self.bildiris_goster("❌ Proqramçı olmaq üçün mütləq universiteti bitirməlisən!")
                return
            if self.dialog: self.dialog.dismiss()
            self.is_unvani = unvan
            self.maas = maas_miqdari
            self.bildiris_goster(f"💼 Təbriklər! '{unvan}' olaraq işə başladın. İllik maaşın sayəsində hər il {maas_miqdari} AZN qazanacaqsan.")
            self.update_stats()

        b1 = MDButton(on_release=lambda x: ise_gir("Kuryer", 50))
        b1.add_widget(MDButtonText(text="🛵 Kuryer (50 AZN/il)"))
        
        b2 = MDButton(on_release=lambda x: ise_gir("Taksi Sürücüsü", 150))
        b2.add_widget(MDButtonText(text="🚕 Taksi Sürücüsü (150 AZN/il)"))

        b3 = MDButton(on_release=lambda x: ise_gir("Proqramçı", 400))
        b3.add_widget(MDButtonText(text="💻 Proqramçı (400 AZN/il - Universitet Tələb Olunur)"))

        btn_list = [b1, b2, b3]

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="İş seçimi edin:"),
            MDDialogButtonContainer(*btn_list)
        )
        self.dialog.open()

    def mulk_marketi(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return

        def al_masin(ad, qiymet):
            if self.dialog: self.dialog.dismiss()
            if self.pul >= qiymet:
                self.pul -= qiymet
                self.masinlar.append(ad)
                self.bildiris_goster(f"🚗 {ad} markalı maşın aldın!")
            else:
                self.bildiris_goster("❌ Pulun çatmır! (0 AZN ilə başlamısan, əvvəlcə pul qazanmalısan)")
            self.update_stats()

        b1 = MDButton(on_release=lambda x: al_masin("VAZ 2107", 2000))
        b1.add_widget(MDButtonText(text="🚗 VAZ 2107 (2000 AZN)"))
        b2 = MDButton(on_release=lambda x: al_masin("BMW E39", 8000))
        b2.add_widget(MDButtonText(text="🏎️ BMW E39 (8000 AZN)"))
        b3 = MDButton(on_release=lambda x: al_masin("Mercedes G63", 25000))
        b3.add_widget(MDButtonText(text="🚙 Mercedes G63 (25000 AZN)"))

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Avtomobil Marketi:"),
            MDDialogButtonContainer(b1, b2, b3)
        )
        self.dialog.open()

    def xestexana(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return
        if self.pul >= 200:
            self.pul -= 200
            self.can = 100
            self.xestelik = "Sağlam"
            self.bildiris_goster("🏥 Xəstəxanada müalicə aldın, bütün canın bərpa olundu! (-200 AZN)")
        else:
            self.bildiris_goster("❌ Müalicə üçün 200 AZN lazımdır.")
        self.update_stats()

    def eylence_menusu(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return

        def eylence_sec(yer, xos_qazanc, qiymet):
            if self.dialog: self.dialog.dismiss()
            if self.pul >= qiymet:
                self.pul -= qiymet
                self.xosbextlik = min(100, self.xosbextlik + xos_qazanc)
                self.bildiris_goster(f"🎉 {yer} getdin, xoşbəxtliyin artdı! (-{qiymet} AZN)")
            else:
                self.bildiris_goster(f"❌ {yer} üçün {qiymet} AZN lazımdır! (Pulun çatmır)")
            self.update_stats()

        b1 = MDButton(on_release=lambda x: eylence_sec("Çayxana", 20, 20))
        b1.add_widget(MDButtonText(text="🍵 Çayxana (20 AZN, +Xoşbəxtlik)"))
        
        b2 = MDButton(on_release=lambda x: eylence_sec("Kino", 30, 40))
        b2.add_widget(MDButtonText(text="🎬 Kino (40 AZN, +Xoşbəxtlik)"))

        b3 = MDButton(on_release=lambda x: eylence_sec("Klub", 40, 80))
        b3.add_widget(MDButtonText(text="🪩 Klub (80 AZN, +Xoşbəxtlik)"))

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Haraya getmək istəyirsən?"),
            MDDialogButtonContainer(b1, b2, b3)
        )
        self.dialog.open()

    def mal_sat(self, instance):
        if self.sigaret > 0:
            kazanc = self.sigaret * 10
            self.pul += kazanc
            say = self.sigaret
            self.sigaret = 0
            self.bildiris_goster(f"📦 {say} ədəd oğurlanan malı satıb {kazanc} AZN qazandın.")
        else:
            self.bildiris_goster("❌ İnventarında satılacaq mal yoxdur.")
        self.update_stats()

    def qara_bazar_menusu(self, instance):
        if self.can <= 0 or self.hebsxanadadir: return

        def al_mehsul(mehsul_adi, qiymet):
            if self.dialog: self.dialog.dismiss()
            if self.pul >= qiymet:
                self.pul -= qiymet
                if mehsul_adi == "Silah":
                    self.silah_sayi += 1
                elif mehsul_adi == "Meth":
                    self.meth += 1
                    self.xosbextlik = min(100, self.xosbextlik + 30)
                elif mehsul_adi == "Bıçaq":
                    self.bicag_sayi += 1
                elif mehsul_adi == "Siqaret":
                    self.sigaret += 1
                    self.xosbextlik = min(100, self.xosbextlik + 10)
                elif mehsul_adi == "Pivə":
                    self.pive += 1
                    self.xosbextlik = min(100, self.xosbextlik + 15)
                
                self.bildiris_goster(f"💣 Qara bazardan {qiymet} AZN ödəyərək {mehsul_adi} aldın!")
            else:
                self.bildiris_goster(f"❌ {mehsul_adi} almaq üçün {qiymet} AZN lazımdır! (0 AZN ilə başlamısan)")
            self.update_stats()

        b1 = MDButton(on_release=lambda x: al_mehsul("Silah", 500))
        b1.add_widget(MDButtonText(text="🔫 Silah (500 AZN)"))
        
        b2 = MDButton(on_release=lambda x: al_mehsul("Meth", 1200))
        b2.add_widget(MDButtonText(text="💊 Meth (1200 AZN, +Xoşbəxtlik)"))

        b3 = MDButton(on_release=lambda x: al_mehsul("Bıçaq", 100))
        b3.add_widget(MDButtonText(text="🔪 Bıçaq (100 AZN)"))

        b4 = MDButton(on_release=lambda x: al_mehsul("Siqaret", 10))
        b4.add_widget(MDButtonText(text="🚬 Siqaret (10 AZN, +Xoşbəxtlik)"))

        b5 = MDButton(on_release=lambda x: al_mehsul("Pivə", 25))
        b5.add_widget(MDButtonText(text="🍺 Pivə (25 AZN, +Xoşbəxtlik)"))

        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Qara Bazar - Nə almaq istəyirsən?"),
            MDDialogButtonContainer(b1, b2, b3, b4, b5)
        )
        self.dialog.open()

    def hebsden_qac(self, instance):
        if random.randint(1, 100) <= 30:
            self.hebsxanadadir = False
            self.ceza_muddeti = 0
            self.bildiris_goster("🏃 Mükəmməl planla həbsxanadan qaçmağı bacardın!")
        else:
            self.ceza_muddeti += 1
            self.bildiris_goster("🚨 Qaçış cəhdin uğursuz oldu! Mühafizəçilər səni tutub cəzanı 1 il uzatdılar.")
        self.refresh_buttons()
        self.update_stats()

class BitLifeApp(MDApp):
    def build(self):
        self.title = "AZE SİMULASYONU"
        return GameScreen()

if __name__ == "__main__":
    BitLifeApp().run()