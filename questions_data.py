"""Answer pages: one real investor question per page. Facts checked against the sources listed on each page.
Edit here, then run build.py. Keep answers answer-first (40 to 70 words), dated, sourced, and educational."""

UPDATED = '2026-10-23'
UPDATED_TEXT = 'October 23, 2026'

QUESTIONS = [
    dict(
        slug='can-foreigners-buy-property-in-colombia',
        q='Can foreigners buy property in Colombia?',
        short='Yes, with the same ownership rights as Colombians, if the money comes in through the formal exchange market and is registered.',
        answer=("Yes. Foreigners can buy and own property in Colombia with the same rights as Colombian citizens. The key step is how the money "
                "arrives: funds should come in through a Colombian bank or other authorized exchange intermediary so the purchase is registered "
                "with Banco de la República as a foreign investment. That registration protects your right to take the money back out when you sell."),
        sections=[
            ('Do you need residency or a visa to buy?',
             "No visa or residency is needed to buy. A passport is used to sign the deed at the notary. Owning property does not by itself give you "
             "the right to live in Colombia; that is a separate visa process."),
            ('Why the way you send money matters',
             "Under Colombia's foreign exchange rules, an investment by a non-resident is registered with Banco de la República through the bank "
             "or exchange intermediary that receives the funds. Registration gives access to the foreign exchange market to send proceeds and "
             "profits abroad later. Money that arrives informally can be hard to repatriate legally."),
            ('What to check before you sign',
             "Ask for the certificado de tradición y libertad, which shows the title history and any liens. Confirm the property tax (predial) and "
             "building fees are paid up to date. If the unit is in a building or gated community, read the propiedad horizontal rules and recent "
             "assembly minutes."),
        ],
        faqs=[
            ('Do foreigners pay more tax than Colombians when they buy?',
             "Closing costs are the same for any buyer. Tax on rent and on a later sale depends on whether you are a tax resident of Colombia."),
            ('Can a foreigner get a mortgage in Colombia?',
             "Some Colombian banks lend to foreigners, usually with a larger down payment and proof of income. Terms vary by bank, so ask several."),
        ],
        sources=[
            ('ProColombia: How to register a foreign investment in Colombia', 'https://investincolombia.com.co/en/resources/how-to-register-a-foreign-investment-in-colombia'),
            ('Decreto 119 de 2017 (foreign investment regime), Función Pública', 'https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=187748'),
            ('Banco de la República: guide to the international investment registration declaration', 'https://www.banrep.gov.co/sites/default/files/guia-diligenciar-declaracion-de-registro-de-inversiones-internacionales.pdf'),
        ],
        related=['register-foreign-investment-in-colombia', 'taxes-foreigners-pay-on-property-in-colombia', 'colombia-investor-visa-through-real-estate'],
    ),
    dict(
        slug='register-foreign-investment-in-colombia',
        q='Why do you have to register a foreign investment in Colombia?',
        short='Registration with Banco de la República is what protects your right to move the money and the sale proceeds back out.',
        answer=("Registering a foreign investment with Banco de la República is what protects your right to send money back out of Colombia. "
                "When the funds arrive through a bank or authorized exchange intermediary, that intermediary reports the investment to the central "
                "bank. A registered investment gives access to the foreign exchange market for profits and sale proceeds. Unregistered money can be "
                "hard to repatriate legally."),
        sections=[
            ('How registration happens',
             "For investments made in foreign currency, the money is channelled through a foreign exchange market intermediary, usually a "
             "commercial bank. The investor gives the bank the required information and the bank reports the transaction to Banco de la República. "
             "ProColombia notes that an exchange declaration is still commonly used in practice."),
            ('What registration protects',
             "Registration protects the investor's rights when profits, proceeds or divestment amounts are sent abroad, and gives access to the "
             "foreign exchange market to bring funds in and transfer them out."),
            ('Why it matters for a visa',
             "Investor visas based on real estate require the investment to be registered with Banco de la República. Simply wiring money is not "
             "enough; the visa file needs the central bank record of the real estate investment in your name."),
        ],
        faqs=[
            ('Who files the registration?',
             "In the common case of an international wire, the receiving bank or exchange intermediary reports it to Banco de la República using information you provide."),
            ('Can you fix an investment that was not registered?',
             "Sometimes, but it is harder after the fact. Ask a Colombian foreign exchange lawyer before you send the money, not after."),
        ],
        sources=[
            ('ProColombia: How to register a foreign investment in Colombia', 'https://investincolombia.com.co/en/resources/how-to-register-a-foreign-investment-in-colombia'),
            ('Decreto 119 de 2017, Función Pública', 'https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=187748'),
            ('Castrillón y Cárdenas: Colombia investor visa requirements', 'https://www.castrillonycardenas.com/visa-de-inversionista-colombia/'),
        ],
        related=['can-foreigners-buy-property-in-colombia', 'colombia-investor-visa-through-real-estate', 'how-the-exchange-rate-changes-your-real-estate-return'],
    ),
    dict(
        slug='taxes-foreigners-pay-on-property-in-colombia',
        q='What taxes do foreigners pay on property in Colombia?',
        short='Closing costs when you buy, annual predial while you own, tax on rent, and 15% capital gains tax when you sell after two years.',
        answer=("A foreign owner meets four kinds of tax in Colombia: closing costs at purchase, annual property tax (predial) while holding, income "
                "tax on rent, and tax on the gain when selling. For 2026, non-residents pay 35% on Colombian-source income such as rent, and a gain "
                "on property held more than two years is taxed as an occasional gain at 15%."),
        sections=[
            ('When you buy',
             "Typical closing costs include notary fees of about 0.54% of the price, usually split between buyer and seller, plus VAT on those fees; "
             "the departmental registration tax of roughly 1.67%, which varies by department and is usually paid by the buyer; and registry fees. "
             "Confirm exact amounts with the notary before signing."),
            ('While you own',
             "The municipality charges an annual property tax, the impuesto predial, based on the cadastral value. Rates are set by each municipal "
             "council. A paid-up predial certificate is needed to sell."),
            ('When you rent it out',
             "Rent is Colombian-source income. KPMG's 2026 guide puts the income tax rate for foreign non-residents at 35 percent. Tax residents "
             "are taxed at progressive rates instead. Residency is generally triggered by more than 183 days in Colombia within a 365-day period."),
            ('When you sell',
             "The seller has 1% of the price withheld at the notary as an advance on income tax. A gain on property held more than two years is "
             "taxed as an occasional gain at 15%. If held two years or less, the gain is taxed as ordinary income."),
        ],
        faqs=[
            ('Is the 1% withholding the final tax on a sale?',
             "No. It is an advance credited against the final income or occasional gains tax for the year."),
            ('Do I also owe tax at home?',
             "Often yes. Many countries, including the United States, tax their residents or citizens on worldwide income. Ask a cross-border tax adviser."),
        ],
        sources=[
            ('KPMG: Taxation of international executives, Colombia (January 2026)', 'https://assets.kpmg.com/content/dam/kpmgsites/xx/pdf/2023/01/TIES-Colombia.pdf.coredownload.inline.pdf'),
            ('Ley 2277 de 2022 (tax reform), Función Pública', 'https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=199883'),
            ('Felix Trujillo Falla: taxes on buying and selling property in Colombia, 2026', 'https://felixtrujillofalla.com/impuestos-compra-venta-inmuebles-colombia-2026/'),
        ],
        related=['can-foreigners-buy-property-in-colombia', 'how-the-exchange-rate-changes-your-real-estate-return', 'what-is-propiedad-horizontal-in-colombia'],
    ),
    dict(
        slug='how-the-exchange-rate-changes-your-real-estate-return',
        q='How does the exchange rate change your return on property abroad?',
        short='Your return is the local price change plus or minus the currency move. A strong local gain can disappear when converted home.',
        answer=("If you earn and spend in dollars but own an asset priced in pesos, your real return is the local price change combined with the "
                "currency move. A property can rise in pesos and still lose value in dollars if the peso weakens. It can also gain in dollars while "
                "flat in pesos if the peso strengthens. The exchange rate is part of the investment, not a side detail."),
        sections=[
            ('A simple example (illustrative numbers)',
             "Say you buy for 400 million pesos when one dollar buys 4,000 pesos: a cost of 100,000 dollars. Five years later you sell for 480 million "
             "pesos, a 20% gain in pesos. If the dollar then buys 4,800 pesos, you receive 100,000 dollars: no gain at home. If it buys 3,600 pesos, "
             "you receive about 133,000 dollars: a 33% gain. Same property, three different results."),
            ('What moves the exchange rate',
             "Interest rate differences between the two central banks, commodity prices for an exporter like Colombia, the current account, political "
             "and policy risk, and global risk appetite all move the peso. None of these can be predicted with certainty, which is why the currency "
             "has to be part of the evaluation."),
            ('How investors manage it',
             "Some match currencies, for example earning local rent to cover local costs. Some size the position so a currency swing is survivable. "
             "Some time purchases and sales against long-term ranges rather than headlines. Each approach has trade-offs."),
        ],
        faqs=[
            ('Does rent in pesos protect me from currency risk?',
             "Partly. It covers local costs, but when you convert rent home the same exchange-rate effect applies."),
            ('Can I hedge the peso?',
             "Hedging tools exist for larger amounts, but they carry costs. Most individual buyers manage currency risk through sizing and timing instead."),
        ],
        sources=[
            ('Banco de la República: what the TRM (official peso-dollar rate) is', 'https://www.banrep.gov.co/es/glosario/tasa-cambio-trm'),
            ('Banco de la República: how to look up historical TRM data', 'https://www.banrep.gov.co/es/como-consultar-datos-historicos-tasa-representativa-mercado-trm-nuevo-portal-estadisticas'),
        ],
        related=['currency-political-and-structural-arbitrage', 'how-to-evaluate-a-country-before-investing', 'taxes-foreigners-pay-on-property-in-colombia'],
    ),
    dict(
        slug='colombia-investor-visa-through-real-estate',
        q='Can buying property in Colombia get you a visa?',
        short='It can support an M investor visa if the property is worth at least 350 monthly minimum wages, in your name, and registered with the central bank.',
        answer=("Buying property can support Colombia's M (migrant) investor visa. Under Cancillería Resolution 5477 of 2022, the property must be "
                "in your name alone, worth at least 350 legal monthly minimum wages (SMMLV) measured at the date you apply, and registered as a "
                "foreign investment with Banco de la República. Meeting the amount does not guarantee approval; Cancillería decides each case."),
        sections=[
            ('What the file usually needs',
             "Proof of ownership, the Banco de la República record showing the real estate investment in your name, a valid passport and the other "
             "documents Cancillería lists for the visa type. Check the current list on Cancillería's site before you apply."),
            ('From M visa to residency',
             "After holding an investor M visa for the required time, a foreigner can apply for an R (resident) visa by accumulated time. Rules and "
             "amounts change, so confirm the current resolution."),
            ('Common mistakes',
             "Buying jointly with a non-applicant, sending money informally so the investment is not registered, or measuring the amount with last "
             "year's minimum wage instead of the value on the application date."),
        ],
        faqs=[
            ('Does the property have to be in my name only?',
             "For the real estate route described by Castrillón y Cárdenas, yes: the property must be in the applicant's exclusive name."),
            ('How much is 350 SMMLV?',
             "It depends on the minimum wage in force on your application date, which changes every year. Multiply the current SMMLV by 350."),
        ],
        sources=[
            ('Resolución 5477 de 2022, SUIN-Juriscol', 'https://www.suin-juriscol.gov.co/viewDocument.asp?ruta=Resolucion/30052890'),
            ('Castrillón y Cárdenas: Colombia investor visa requirements and amounts', 'https://www.castrillonycardenas.com/visa-de-inversionista-colombia/'),
        ],
        related=['register-foreign-investment-in-colombia', 'can-foreigners-buy-property-in-colombia', 'how-to-evaluate-a-country-before-investing'],
    ),
    dict(
        slug='what-is-propiedad-horizontal-in-colombia',
        q='What is propiedad horizontal in Colombia?',
        short='The legal regime for buildings and gated communities: you own your unit, share the common areas, and pay a mandatory administration fee.',
        answer=("Propiedad horizontal is the legal regime, set by Law 675 of 2001, for apartment buildings and gated communities in Colombia. You own "
                "your unit outright and share ownership of the common areas with the other owners. Every owner pays a monthly administration fee "
                "(cuota de administración), and the building is run by an owners' assembly, an administrator and its own internal rules."),
        sections=[
            ('What the administration fee pays for',
             "Security, cleaning, maintenance of shared areas, insurance and the building's reserve fund. Fees vary widely with amenities and size, "
             "and unpaid fees can be collected through legal action."),
            ('Rules that affect investors',
             "The building's reglamento can limit uses such as short-term rentals, pets or renovations. Read it, and the last assembly minutes, "
             "before buying. They show disputes, planned special assessments and how well the building is run."),
            ('Questions to ask the administrator',
             "Is the unit paid up? Are any special assessments (cuotas extraordinarias) approved or planned? How large is the reserve fund? Are "
             "short-term rentals allowed?"),
        ],
        faqs=[
            ('Is the administration fee optional?',
             "No. It is an obligation of every owner under the building's regime and can be collected through the courts if unpaid."),
            ('Who decides big repairs?',
             "The owners' assembly approves budgets and special assessments according to the building's rules and Law 675."),
        ],
        sources=[
            ('Ministerio de Vivienda: Propiedad horizontal guide (PDF)', 'https://minvivienda.gov.co/sites/default/files/2020-07/cartilla-propiedad-horizontal-web.pdf'),
        ],
        related=['can-foreigners-buy-property-in-colombia', 'taxes-foreigners-pay-on-property-in-colombia', 'how-to-evaluate-a-country-before-investing'],
    ),
    dict(
        slug='currency-political-and-structural-arbitrage',
        q='What are currency, political and structural arbitrage?',
        short='Three reasons the same money can buy more abroad, and three matching risks that decide whether the gap is real.',
        answer=("They are three reasons the same savings can buy more in one country than another. Currency arbitrage comes from exchange rates. "
                "Political arbitrage comes from markets that price in more risk than exists. Structural arbitrage comes from rules on ownership, tax "
                "and repatriation. Each gap carries a matching risk, so the work is telling a real opportunity from a mispriced one."),
        sections=[
            ('Currency',
             "A strong home currency buys more local assets. The same exchange rate can move against you while you hold, so the currency is part of "
             "the return, not a constant."),
            ('Political',
             "Markets that headlines avoid can be priced below their real risk. Sometimes they are priced correctly, or too high. Research separates "
             "the two."),
            ('Structural',
             "Ownership rules, taxes, registration and the ability to bring money home decide what you actually keep. These rules differ by country "
             "and change over time."),
        ],
        faqs=[
            ('Is arbitrage risk-free?',
             "No. In this sense it means a price gap between markets. Every gap has a reason, and the reason is the risk."),
            ('Which matters most?',
             "It depends on the deal. For most buyers paying in dollars, currency has the largest effect on the final result."),
        ],
        sources=[],
        related=['how-the-exchange-rate-changes-your-real-estate-return', 'how-to-evaluate-a-country-before-investing', 'taxes-foreigners-pay-on-property-in-colombia'],
    ),
    dict(
        slug='how-to-evaluate-a-country-before-investing',
        q='How do you evaluate a country before investing there?',
        short='Information, evaluation, interpretation, then action: gather sourced facts, test them, read what they mean for you, and only then commit.',
        answer=("Use four steps in order. Information: gather sourced facts on the currency, politics, ownership rules and taxes. Evaluation: test "
                "those facts against each other and against your own income currency and time horizon. Interpretation: decide what they mean for "
                "your situation. Action: commit only after the first three, and before the opportunity becomes common knowledge."),
        sections=[
            ('Information',
             "Start with primary sources: the central bank, the tax authority, the foreign ministry and the laws themselves. Use secondary sources to "
             "find questions, not answers."),
            ('Evaluation',
             "Run the numbers in your home currency. Stress-test them: what happens if the currency weakens 20%, if rent is 30% lower, if a sale takes "
             "a year?"),
            ('Interpretation',
             "The same facts mean different things to a retiree on a fixed dollar income and to a family office with a 20-year horizon. Decide which "
             "risks you can carry."),
            ('Action',
             "By the time an opportunity is on the news, it is usually in the price. Acting early is only an edge if the first three steps were done."),
        ],
        faqs=[
            ('Do I need to visit before investing?',
             "Seeing the market in person catches things documents miss: the street, the building, the neighbours, the commute. Most experienced investors visit."),
            ('Where can I learn this in practice?',
             "Tierra Firme covers it on the show and in small seminars in Bogotá. Join the list for dates."),
        ],
        sources=[],
        related=['currency-political-and-structural-arbitrage', 'how-the-exchange-rate-changes-your-real-estate-return', 'can-foreigners-buy-property-in-colombia'],
    ),
]
