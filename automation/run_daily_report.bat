@echo off

cd /d "C:\Users\HP\OneDrive\Desktop\ABDULLAH\DA\Retail-Sales-E-Commerce-Analytics-Dashboard"

echo ==========================================
echo Automated Daily Sales Reporting
echo ==========================================

echo.
echo Running report for latest available data...
echo.

python -c "from automation.database import get_connection; c=get_connection(); cur=c.cursor(); cur.execute('SELECT MAX(DATE(order_purchase_timestamp)) FROM ecommerce_dashboard'); d=cur.fetchone()[0]; cur.close(); c.close(); print(d)" > automation\latest_date.txt

set /p REPORT_DATE=<automation\latest_date.txt

echo Report Date: %REPORT_DATE%
echo.

python -m automation.runner %REPORT_DATE%

echo.
echo ==========================================
echo Automation completed
echo ==========================================

exit /b %ERRORLEVEL%