import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from PIL import Image
import base64
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Fintro - Learn About ETFs",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
def local_css():
    st.markdown("""
    <style>
    /* Main colors */
    :root {
        --primary-blue: #1A2980;
        --primary-teal: #26D0CE;
        --light-gray: #F5F7FA;
        --white: #FFFFFF;
        --coral: #FF6B6B;
        --low-risk: #4CAF50;
        --medium-risk: #FFC107;
        --high-risk: #F44336;
    }
    
    .main {
        background-color: var(--light-gray);
        padding: 20px;
    }
    
    h1, h2, h3 {
        color: var(--primary-blue);
    }
    
    .stButton>button {
        background-color: var(--coral);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        transition-duration: 0.4s;
    }
    
    .stButton>button:hover {
        background-color: #ff5252;
        transform: translateY(-2px);
    }
    
    /* Card styling */
    .card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Profile Card */
    .profile-card {
        display: flex;
        gap: 20px;
    }
    
    .profile-visual {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7F7FD5, #86A8E7, #91EAE4);
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2rem;
    }
    
    /* ETF Card */
    .etf-card {
        display: flex;
        border-radius: 8px;
        overflow: hidden;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    .etf-match-score {
        width: 70px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: linear-gradient(to bottom, var(--primary-blue), var(--primary-teal));
        color: white;
        padding: 15px 10px;
    }
    
    /* Chat styling */
    .chat-message {
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
    }

    .chat-message.user {
        background-color: var(--primary-teal);
        color: white;
        border-bottom-right-radius: 5px;
        align-self: flex-end;
        margin-left: 50px;
    }

    .chat-message.bot {
        background-color: #f0f0f0;
        border-bottom-left-radius: 5px;
        align-self: flex-start;
        margin-right: 50px;
    }
    
    /* Risk level styling */
    .risk-low {
        background-color: var(--low-risk);
    }
    
    .risk-medium {
        background-color: var(--medium-risk);
    }
    
    .risk-high {
        background-color: var(--high-risk);
    }

    /* Table styling */
    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        width: 100%;
    }

    .styled-table thead tr {
        background-color: var(--primary-blue);
        color: white;
        text-align: left;
    }

    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    /* Time filter buttons */
    .time-filter-container {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
    }

    .time-filter {
        padding: 5px 15px;
        border-radius: 20px;
        background-color: #f0f0f0;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .time-filter.active {
        background-color: var(--primary-blue);
        color: white;
    }
    
    /* FAQ Card Styling */
    .faq-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin-bottom: 10px;
    }
    
    .faq-question {
        font-weight: 600;
        margin-bottom: 8px;
        color: var(--primary-blue);
    }
    
    /* Metric styling */
    .metric-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    
    .metric {
        text-align: center;
        flex: 1;
    }
    
    .metric-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary-blue);
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #666;
    }
    
    /* Positive/Negative values */
    .positive {
        color: var(--low-risk);
        font-weight: 600;
    }
    
    .negative {
        color: var(--high-risk);
        font-weight: 600;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(to right, var(--primary-blue), var(--primary-teal));
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo {
        font-size: 1.5rem;
        font-weight: 700;
        display: flex;
        align-items: center;
    }
    
    .logo-icon {
        margin-right: 8px;
    }
    
    /* Make the sidebar narrower */
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 200px;
        max-width: 200px;
    }
    
    /* Hide the Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Call the function to apply CSS
local_css()

# Initialize session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'recommendations'
if 'risk_tolerance' not in st.session_state:
    st.session_state.risk_tolerance = 6
if 'investment_amount' not in st.session_state:
    st.session_state.investment_amount = 2500
if 'profile' not in st.session_state:
    st.session_state.profile = 'Novice Aggressive'
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'selected_time_period' not in st.session_state:
    st.session_state.selected_time_period = '6M'
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [{"sender": "bot", "text": "Hi there! I'm your Fintro assistant. Ask me anything about ETFs, investing, or financial concepts!"}]

# Sample ETF data
etfs = [
    {
        "id": 1,
        "name": "Iota ETF",
        "ticker": "IETF",
        "category": "Equity",
        "annualReturn": 12.77,
        "expenseRatio": 0.36,
        "volatility": 12.1,
        "riskLevel": 8,
        "matchScore": 92,
        "returns": {"1M": 1.2, "3M": 3.6, "6M": 6.8, "1Y": 12.77, "5Y": 64.3}
    },
    {
        "id": 2,
        "name": "Epsilon ETF",
        "ticker": "EPSN",
        "category": "Equity",
        "annualReturn": 2.59,
        "expenseRatio": 0.49,
        "volatility": 6.7,
        "riskLevel": 7,
        "matchScore": 85,
        "returns": {"1M": 0.1, "3M": 0.8, "6M": 1.4, "1Y": 2.59, "5Y": 13.5}
    },
    {
        "id": 3,
        "name": "Alpha ETF",
        "ticker": "ALFA",
        "category": "Bond",
        "annualReturn": 9.77,
        "expenseRatio": 0.26,
        "volatility": 8.5,
        "riskLevel": 5,
        "matchScore": 75,
        "returns": {"1M": 0.7, "3M": 2.3, "6M": 4.7, "1Y": 9.77, "5Y": 48.2}
    },
    {
        "id": 4,
        "name": "Delta ETF",
        "ticker": "DTEF",
        "category": "Mixed",
        "annualReturn": 8.25,
        "expenseRatio": 0.31,
        "volatility": 7.9,
        "riskLevel": 6,
        "matchScore": 70,
        "returns": {"1M": 0.9, "3M": 2.5, "6M": 4.1, "1Y": 8.25, "5Y": 42.8}
    }
]

# User profile data
user_profile = {
    "name": "Alex Johnson",
    "email": "alex.j@university.edu",
    "portfolioValue": "€3,742.50",
    "totalInvested": "€3,500.00",
    "totalReturn": "€242.50 (6.93%)",
    "watchlist": [
        {"name": "Delta ETF", "ticker": "DTEF", "change": "+2.4%"},
        {"name": "Sigma ETF", "ticker": "SGETF", "change": "-0.7%"},
        {"name": "Omega ETF", "ticker": "OMGA", "change": "+1.2%"}
    ],
    "recentActivity": [
        {"date": "Oct 5, 2024", "action": "Purchased Alpha ETF", "amount": "€500.00"},
        {"date": "Sept 28, 2024", "action": "Dividend Payment", "amount": "€12.75"},
        {"date": "Sept 15, 2024", "action": "Purchased Iota ETF", "amount": "€750.00"}
    ],
    "holdings": [
        {"name": "Alpha ETF", "ticker": "ALFA", "shares": "12.5", "value": "€1,221.75", "allocation": "32.6%"},
        {"name": "Iota ETF", "ticker": "IETF", "shares": "18.2", "value": "€2,243.40", "allocation": "59.9%"},
        {"name": "Cash", "ticker": "-", "shares": "-", "value": "€277.35", "allocation": "7.5%"}
    ]
}

# Chatbot responses
chatbot_responses = {
    "what is an etf": "An ETF (Exchange-Traded Fund) is an investment fund that trades on stock exchanges, much like stocks. ETFs hold assets such as stocks, bonds, or commodities, and trade at market-determined prices. They typically have higher daily liquidity and lower fees than mutual funds, making them attractive for individual investors.",
    "what exactly is an etf": "An ETF (Exchange-Traded Fund) is an investment fund that trades on stock exchanges, much like stocks. ETFs hold assets such as stocks, bonds, or commodities, and trade at market-determined prices. They typically have higher daily liquidity and lower fees than mutual funds, making them attractive for individual investors.",
    "how do etfs work": "ETFs work by pooling money from many investors to buy a diversified portfolio of assets. When you buy shares of an ETF, you're buying a small portion of the entire portfolio. ETFs trade throughout the day like stocks, with prices that fluctuate based on supply and demand. Most ETFs are designed to track an index, sector, commodity, or other asset but can be bought and sold like a common stock.",
    "what are the benefits of etfs": "ETFs offer several advantages: 1) Diversification - instant exposure to many stocks or bonds, 2) Low costs - typically lower expense ratios than mutual funds, 3) Tax efficiency - generally trigger fewer capital gains, 4) Liquidity - can be bought and sold throughout the trading day, 5) Transparency - holdings are disclosed daily, and 6) Flexibility - can be used for various investment strategies including long-term investing.",
    "what's the difference between etfs and mutual funds": "The main differences between ETFs and mutual funds are: 1) Trading - ETFs trade like stocks throughout the day while mutual funds trade once per day after market close, 2) Fees - ETFs typically have lower expense ratios, 3) Tax efficiency - ETFs are usually more tax-efficient, 4) Minimum investment - ETFs have no minimums beyond the share price, while mutual funds often require minimum investments, and 5) Management style - most ETFs are passively managed while mutual funds are often actively managed.",
    "what are index etfs": "Index ETFs are exchange-traded funds designed to track a specific market index, such as the S&P 500 or NASDAQ. They aim to replicate the performance of their target index by holding all (or a representative sample) of the securities in the index. Index ETFs offer low-cost diversification and typically have lower expense ratios than actively managed funds because they simply follow an index rather than paying managers to select investments.",
    "what are the risks of etfs": "The main risks of ETFs include: 1) Market risk - ETF prices fluctuate with their underlying assets, 2) Tracking error risk - some ETFs may not perfectly match their benchmark index, 3) Liquidity risk - some specialized ETFs may have lower trading volumes, 4) Concentration risk - sector or country-specific ETFs lack broad diversification, 5) Currency risk - international ETFs may be affected by exchange rate fluctuations, and 6) Trading costs - frequent buying and selling can add costs through bid-ask spreads and commissions.",
    "how do i buy an etf": "You can buy ETFs through most brokerage accounts, including traditional brokers and online platforms. The process is similar to buying stocks: 1) Open a brokerage account if you don't have one, 2) Fund your account, 3) Research ETFs that match your investment goals, 4) Place an order using the ETF's ticker symbol, and 5) Specify the number of shares or amount you wish to invest. ETFs trade at market prices throughout the trading day, so you can buy them whenever the market is open.",
    "what is an expense ratio": "An expense ratio is the annual fee that ETFs and mutual funds charge shareholders for managing the fund. It's expressed as a percentage of the fund's average net assets. For example, an expense ratio of 0.5% means that for every $1,000 invested, you pay $5 annually in fees. ETFs typically have lower expense ratios than mutual funds, especially passive index ETFs. The expense ratio is important because higher fees directly reduce your investment returns over time.",
    "how are etfs taxed": "ETFs are generally more tax-efficient than mutual funds. When you hold ETFs: 1) Dividends and capital gain distributions are taxable in the year they're received, 2) When you sell ETF shares at a profit, you'll owe capital gains tax based on how long you held them (short-term or long-term rates), 3) ETFs typically generate fewer capital gain distributions than mutual funds due to their unique creation/redemption process, making them more tax-efficient for long-term investors. Tax laws vary by country, so consult a tax professional for specific advice.",
    "what is the difference between active and passive etfs": "Passive ETFs aim to track a specific index or benchmark, while active ETFs have portfolio managers who make investment decisions to try to outperform the market. Key differences: 1) Management style - passive ETFs follow a rules-based approach while active ETFs rely on manager expertise, 2) Expense ratios - passive ETFs typically have lower fees than active ETFs, 3) Trading activity - active ETFs generally have higher turnover, 4) Performance goals - passive ETFs seek to match their benchmark's performance, while active ETFs aim to exceed it, and 5) Transparency - passive ETFs disclose holdings daily, while some active ETFs may disclose less frequently.",
    "what are the different types of etfs": "The main types of ETFs include: 1) Stock (equity) ETFs - track stock indices, sectors, or investment strategies, 2) Bond (fixed income) ETFs - invest in government, corporate, or municipal bonds, 3) Commodity ETFs - track physical commodities like gold or oil, 4) Currency ETFs - track currency values or baskets of currencies, 5) Specialty ETFs - focus on specific themes like ESG (Environmental, Social, Governance), 6) Inverse ETFs - aim to profit from market declines, 7) Leveraged ETFs - use financial derivatives to amplify returns, and 8) International ETFs - focus on global or country-specific markets outside your home country.",
    "are etfs good for beginners": "Yes, ETFs can be excellent investment vehicles for beginners for several reasons: 1) Instant diversification - a single ETF can give you exposure to hundreds of securities, reducing risk, 2) Low minimum investment - you can start with just the price of one share, 3) Simplicity - index ETFs are straightforward to understand compared to selecting individual stocks, 4) Low costs - many ETFs have very low expense ratios, 5) Liquidity - easy to buy and sell when needed, and 6) Variety - you can start with broad market ETFs and gradually add more specific ones as you learn. For beginners, broad-based index ETFs are often recommended as a core investment."
}

# Helper Functions
def get_risk_level_class(risk_level):
    if risk_level <= 3:
        return "risk-low"
    if risk_level <= 6:
        return "risk-medium"
    return "risk-high"

def get_expected_returns(etf, period):
    return etf["returns"][period]

def get_recommendations():
    # Filter and sort ETFs based on risk tolerance
    risk_tolerance = st.session_state.risk_tolerance
    investment_amount = st.session_state.investment_amount
    
    # Filter based on risk tolerance
    filtered_etfs = etfs.copy()
    if risk_tolerance < 4:
        # Conservative investors prefer bonds and lower volatility
        filtered_etfs = [etf for etf in filtered_etfs if etf["category"] == "Bond" or etf["riskLevel"] < 6]
    elif risk_tolerance > 7:
        # Aggressive investors prefer higher return potential
        filtered_etfs = [etf for etf in filtered_etfs if etf["annualReturn"] > 5]
    
    # Sort by match score
    filtered_etfs.sort(key=lambda x: x["matchScore"], reverse=True)
    
    st.session_state.recommendations = filtered_etfs
    
    # Update profile based on risk tolerance
    if risk_tolerance <= 4:
        st.session_state.profile = "Experienced Conservative" if investment_amount > 3000 else "Novice Conservative"
    elif risk_tolerance <= 7:
        st.session_state.profile = "Experienced Moderate" if investment_amount > 3000 else "Novice Moderate"
    else:
        st.session_state.profile = "Experienced Aggressive" if investment_amount > 3000 else "Novice Aggressive"

def handle_chat_input():
    if st.session_state.chat_input:
        user_message = st.session_state.chat_input
        st.session_state.chat_messages.append({"sender": "user", "text": user_message})
        
        # Process user message and get response
        query = user_message.lower()
        bot_response = "I'm not sure about that. Could you try asking about ETFs, investment basics, or risk profiles?"
        
        # Check for exact matches
        if query in chatbot_responses:
            bot_response = chatbot_responses[query]
        else:
            # Check for key phrases
            key_phrase_matches = {
                "what": {
                    "etf": "what is an etf",
                    "exactly": "what exactly is an etf",
                    "index": "what are index etfs",
                    "risk": "what are the risks of etfs",
                    "expense ratio": "what is an expense ratio",
                    "type": "what are the different types of etfs",
                    "different type": "what are the different types of etfs",
                    "active and passive": "what is the difference between active and passive etfs"
                },
                "how": {
                    "work": "how do etfs work",
                    "buy": "how do i buy an etf",
                    "purchase": "how do i buy an etf",
                    "tax": "how are etfs taxed"
                },
                "benefit": {
                    "": "what are the benefits of etfs"
                },
                "advantage": {
                    "etf": "what are the benefits of etfs"
                },
                "difference": {
                    "mutual fund": "what's the difference between etfs and mutual funds",
                    "active": "what is the difference between active and passive etfs",
                    "passive": "what is the difference between active and passive etfs"
                },
                "vs": {
                    "mutual": "what's the difference between etfs and mutual funds"
                },
                "beginner": {
                    "": "are etfs good for beginners"
                },
                "new": {
                    "investor": "are etfs good for beginners"
                }
            }
            
            # Check if query contains multiple key phrases
            matched = False
            for primary_key, secondary_matches in key_phrase_matches.items():
                if primary_key in query and not matched:
                    for secondary_key, response_key in secondary_matches.items():
                        if (secondary_key == "" or secondary_key in query) and not matched:
                            bot_response = chatbot_responses[response_key]
                            matched = True
        
        # Add bot response after a short delay
        time.sleep(0.6)  # simulate thinking time
        st.session_state.chat_messages.append({"sender": "bot", "text": bot_response})
        
        # Clear the input
        st.session_state.chat_input = ""

def display_chart(recommendations, selected_time_period):
    if not recommendations:
        return
    
    # Prepare data for chart
    etf_names = [etf["name"] for etf in recommendations]
    returns = [etf["returns"][selected_time_period] for etf in recommendations]
    
    # Set colors based on return values
    colors = ["#1976D2", "#7B1FA2", "#FFA000", "#388E3C"][:len(recommendations)]
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(etf_names, returns, color=colors, alpha=0.8)
    
    # Add labels and title
    ax.set_ylabel('Returns (%)')
    ax.set_title(f'Expected Returns ({selected_time_period})')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontweight='bold')
    
    # Customize appearance
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    return fig

# App title and header
st.markdown('<div class="app-header"><div class="logo"><span class="logo-icon">📈</span> Fintro</div></div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio("", ["Recommendations", "Learn", "My Profile"], index=["recommendations", "learn", "profile"].index(st.session_state.active_tab))

# Update active tab based on sidebar selection
st.session_state.active_tab = navigation.lower()

# Main content based on active tab
if st.session_state.active_tab == 'recommendations':
    st.title("Find ETFs that match your investment style with Fintro")
    st.write("Answer a few questions to get personalized ETF recommendations based on your risk tolerance and investment goals.")
    
    # Input section
    col1, col2, col3 = st.columns([3, 3, 2])
    
    with col1:
        st.write("Risk Tolerance (1-10)")
        risk_tolerance = st.slider("", 1, 10, st.session_state.risk_tolerance, key="risk_slider")
        st.session_state.risk_tolerance = risk_tolerance
    
    with col2:
        st.write("Investment Amount (€)")
        investment_amount = st.number_input("", min_value=100, max_value=10000, value=st.session_state.investment_amount, step=100, key="investment_input")
        st.session_state.investment_amount = investment_amount
    
    with col3:
        st.write("")
        st.write("")
        if st.button("Get Recommendations"):
            get_recommendations()
    
    # Profile card
    st.markdown("## Your Investor Profile")
    
    profile_info = {
        'Novice Conservative': {
            'description': 'You prefer stability and are cautious with your investments.',
            'percentage': '11.8%',
            'experience': '0-2 yrs'
        },
        'Novice Moderate': {
            'description': 'You seek a balance between risk and return with limited investment experience.',
            'percentage': '35.2%',
            'experience': '0-2 yrs'
        },
        'Novice Aggressive': {
            'description': 'You have limited experience but are willing to take calculated risks for better returns.',
            'percentage': '27.0%',
            'experience': '0-2 yrs'
        },
        'Experienced Conservative': {
            'description': 'Despite your experience, you prefer consistent returns over high-risk opportunities.',
            'percentage': '5.5%',
            'experience': '3+ yrs'
        },
        'Experienced Moderate': {
            'description': 'You have investment experience and prefer a balanced approach to risk and return.',
            'percentage': '10.3%',
            'experience': '3+ yrs'
        },
        'Experienced Aggressive': {
            'description': 'You have investment experience and are comfortable with higher risk for potentially greater returns.',
            'percentage': '10.2%',
            'experience': '3+ yrs'
        }
    }
    
    profile = st.session_state.profile
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<div style="width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #7F7FD5, #86A8E7, #91EAE4); color: white; display: flex; justify-content: center; align-items: center; font-size: 2rem;">📊</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'### {profile}')
        st.markdown(f'<span style="display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; color: white; background-color: #26D0CE; margin-bottom: 10px;">{profile_info[profile]["percentage"]} of students</span>', unsafe_allow_html=True)
        st.write(profile_info[profile]['description'])
        
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="metric">
            <div class="metric-value">{st.session_state.risk_tolerance}/10</div>
            <div class="metric-label">Risk</div>
        </div>
        <div class="metric">
            <div class="metric-value">{profile_info[profile]['experience']}</div>
            <div class="metric-label">Experience</div>
        </div>
        <div class="metric">
            <div class="metric-value">€{st.session_state.investment_amount}</div>
            <div class="metric-label">Investment</div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ETF Recommendations
    st.markdown("## Top ETF Recommendations")
    
    if not st.session_state.recommendations:
        # Initialize with all ETFs if none are selected yet
        get_recommendations()
    
    for etf in st.session_state.recommendations:
        col1, col2 = st.columns([1, 6])
        
        with col1:
            st.markdown(f'''
            <div style="background: linear-gradient(to bottom, #1A2980, #26D0CE); color: white; padding: 15px; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
                <div style="font-size: 1.5rem; font-weight: 700;">{etf["matchScore"]}%</div>
                <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px;">Match</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div style="background-color: white; padding: 15px; border-radius: 0 8px 8px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div style="font-size: 1.1rem; font-weight: 600;">{etf["name"]} ({etf["ticker"]})</div>
                    <span style="padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; background-color: {'#E3F2FD' if etf["category"] == 'Equity' else '#F3E5F5' if etf["category"] == 'Bond' else '#FFFDE7'}; color: {'#1976D2' if etf["category"] == 'Equity' else '#7B1FA2' if etf["category"] == 'Bond' else '#FFA000'};">{etf["category"]}</span>
                </div>
                
                <div style="display: flex; gap: 15px; margin-bottom: 15px;">
                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #1A2980;">{etf["annualReturn"]}%</div>
                        <div style="font-size: 0.8rem; color: #666;">Annual Return</div>
                    </div>
                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #1A2980;">{etf["expenseRatio"]}%</div>
                        <div style="font-size: 0.8rem; color: #666;">Expense Ratio</div>
                    </div>
                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 1.1rem; font-weight: 600; color: #1A2980;">{etf["volatility"]}%</div>
                        <div style="font-size: 0.8rem; color: #666;">Volatility</div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600; margin-bottom: 5px;">
                        <span>Risk Level</span>
                        <span>{etf["riskLevel"]}/10</span>
                    </div>
                    <div style="height: 6px; background-color: #e0e0e0; border-radius: 3px; overflow: hidden;">
                        <div style="height: 100%; width: {etf["riskLevel"]*10}%; background-color: {
                            '#4CAF50' if etf["riskLevel"] <= 3 else 
                            '#FFC107' if etf["riskLevel"] <= 6 else 
                            '#F44336'
                        }; border-radius: 3px;"></div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Performance Chart
    if st.session_state.recommendations:
        st.markdown("## Performance Comparison")
        
        # Time period selection
        col1, col2, col3, col4, col5 = st.columns(5)
        time_periods = {"1M": col1, "3M": col2, "6M": col3, "1Y": col4, "5Y": col5}
        
        for period, col in time_periods.items():
            with col:
                if st.button(period, key=f"time_{period}", 
                            help=f"Show {period} returns",
                            on_click=lambda p=period: setattr(st.session_state, 'selected_time_period', p),
                            type="secondary" if period != st.session_state.selected_time_period else "primary"):
                    st.session_state.selected_time_period = period
        
        # Display returns data
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"### Expected Returns ({st.session_state.selected_time_period})")
            for etf in st.session_state.recommendations:
                return_value = get_expected_returns(etf, st.session_state.selected_time_period)
                st.markdown(
                    f"**{etf['name']}:** <span class=\"{'positive' if return_value >= 0 else 'negative'}\">{'+'if return_value >= 0 else ''}{return_value}%</span>",
                    unsafe_allow_html=True
                )
        
        with col2:
            # Display chart
            fig = display_chart(st.session_state.recommendations, st.session_state.selected_time_period)
            st.pyplot(fig)

elif st.session_state.active_tab == 'learn':
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("## Fintro Assistant")
        
        # Display chat messages
        for message in st.session_state.chat_messages:
            if message["sender"] == "user":
                st.markdown(f"<div class='chat-message user'>{message['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message bot'>{message['text']}</div>", unsafe_allow_html=True)
        
        # Chat input
        st.text_input("Ask me anything about ETFs...", key="chat_input", on_change=handle_chat_input)
    
    with col2:
        st.markdown("## Frequently Asked Questions")
        
        # FAQ cards
        faqs = [
            {"question": "What is an ETF?", "answer": "An ETF (Exchange-Traded Fund) is an investment fund that trades on stock exchanges, much like stocks. They typically have lower fees than mutual funds."},
            {"question": "How do I choose an ETF?", "answer": "Consider your goals, risk tolerance, the sector the ETF tracks, expense ratio, liquidity, and the fund provider's reputation."},
            {"question": "What's the difference between ETFs and mutual funds?", "answer": "ETFs trade throughout the day like stocks, while mutual funds trade once at market close. ETFs typically have lower fees and more tax efficiency."},
            {"question": "How do ETFs work?", "answer": "ETFs work by pooling money from investors to buy a portfolio of assets. Most ETFs track an index, but some are actively managed."}
        ]
        
        for faq in faqs:
            with st.expander(faq["question"]):
                st.write(faq["answer"])
        
        # Suggested questions
        st.markdown("### Try asking:")
        
        # Create buttons for suggested questions
        suggested_questions = [
            "What exactly is an ETF?", 
            "How do ETFs work?", 
            "What are the benefits of ETFs?",
            "What are the risks of ETFs?",
            "Are ETFs good for beginners?",
            "What is an expense ratio?"
        ]
        
        for question in suggested_questions:
            if st.button(question, key=f"q_{question}"):
                st.session_state.chat_input = question
                handle_chat_input()
                st.experimental_rerun()

elif st.session_state.active_tab == 'profile':
    st.title("My Profile")
    
    # Profile header section
    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
    
    with col1:
        st.markdown('<div style="width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #1A2980, #26D0CE); color: white; display: flex; justify-content: center; align-items: center; font-size: 3rem;">👤</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"## {user_profile['name']}")
        st.markdown(f"<div style='color: #666;'>{user_profile['email']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="margin-top: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600;">Portfolio Value:</span>
                <span>{user_profile['portfolioValue']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600;">Total Invested:</span>
                <span>{user_profile['totalInvested']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600;">Total Return:</span>
                <span style="color: #4CAF50;">{user_profile['totalReturn']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 2rem;">3</div>
            <div style="color: #666;">ETFs Owned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 2rem; color: #4CAF50;">6.93%</div>
            <div style="color: #666;">Total Return</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Holdings section
    st.markdown("## Portfolio Holdings")
    
    holdings_df = pd.DataFrame(user_profile["holdings"])
    st.table(holdings_df)
    
    # Create two columns for watchlist and activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## Your Watchlist")
        watchlist_df = pd.DataFrame(user_profile["watchlist"])
        watchlist_styled = watchlist_df.style.applymap(
            lambda x: 'color: #4CAF50;' if x.startswith('+') else 'color: #F44336;' if x.startswith('-') else '',
            subset=['change']
        )
        st.table(watchlist_styled)
    
    with col2:
        st.markdown("## Recent Activity")
        activity_df = pd.DataFrame(user_profile["recentActivity"])
        st.table(activity_df)

# Footer
st.markdown("""
<div style="margin-top: 50px; text-align: center; color: #666; font-size: 0.8rem;">
    Fintro © 2025 | Educational Platform for Learning about ETFs
</div>
""", unsafe_allow_html=True)
