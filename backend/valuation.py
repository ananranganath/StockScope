def run_dcf(fcf, shares, cash, debt, growth, terminal_growth, discount, years=5):
    """Estimate value per share with a discounted cash flow model.
    fcf              latest yearly free cash flow
    shares           number of shares outstanding
    cash, debt       the company's cash and debt
    growth           yearly FCF growth for the projection years
    terminal_growth  growth forever after that
    discount         the yearly return rate you require
    """
    if fcf <= 0:
        raise ValueError("Free cash flow must be positive for a DCF to make sense.")
    if shares <= 0:
        raise ValueError("Shares outstanding must be positive.")
    if discount <= terminal_growth:
        raise ValueError("Discount rate must be greater than terminal growth rate.")

    total = 0
    for year in range(1, years + 1):
        fcf = fcf * (1 + growth)              # grow this year's cash flow
        total += fcf / (1 + discount)**year   # what it's worth today

    terminal_value = fcf * (1 + terminal_growth) / (discount - terminal_growth)
    total += terminal_value / (1 + discount)**years

    equity_value = total + cash -debt
    return equity_value / shares