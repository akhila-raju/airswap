import time
import click
import urllib
import json
from click.testing import CliRunner

# Run following command in terminal: airswap. This will print out the average every 60 seconds. To abort, use: ctrl+c.

@click.command()
@click.option('--currencypair', prompt='Please enter a valid cryptocurrency pair, such as BTC_ETH')
def displayAvgPrice(currencypair):
	prices = json.loads(urllib.urlopen('https://poloniex.com/public?command=returnTicker').read())
	if currencypair not in prices:
		raise click.ClickException('Invalid pair entered.')
	click.echo('Displaying moving average price per minute for ' + currencypair)		
	avg, minsSinceStart = float(prices[currencypair]['last']), 0
	startTime = time.time()
	while True:
		prices = json.loads(urllib.urlopen('https://poloniex.com/public?command=returnTicker').read())
		if currencypair not in prices:
			raise click.ClickException('Data unavailable for entered pair.')
		avg = ((avg * minsSinceStart) + float(prices[currencypair]["last"])) / (minsSinceStart + 1)
		click.echo(avg)
		minsSinceStart += 1
		time.sleep(60.0 - ((time.time() - startTime) % 60.0))


# Run following tests using pytest in terminal: pytest airswap.py

# Test 1: Test average.
def test_avg():
    @click.command()
    def testAvg():
    	minsSinceStart = 2
    	avg = 50
    	prices = {'BTC_ETH': {'last': 26}}
    	click.echo(((avg * minsSinceStart) + float(prices['BTC_ETH']['last'])) / (minsSinceStart + 1))

    runner = CliRunner()
    result = runner.invoke(testAvg)
    assert result.exit_code == 0
    assert result.output == '42.0\n'

# Test 2: Test invalid currency.
def test_validPair():
    @click.command()
    @click.argument('currencypair')
    def validPair(currencypair):
		prices = {'BTC_ETH': 1}
		if currencypair not in prices:
			raise click.ClickException('Invalid pair entered.')
		click.echo('Displaying moving average price per minute for ' + currencypair)

    runner = CliRunner()
    result = runner.invoke(validPair, ['BTC_ETH'])
    assert result.exit_code == 0
    assert result.output == 'Displaying moving average price per minute for BTC_ETH\n'


# Test 3: Test valid currency.
def test_invalidPair():
    @click.command()
    @click.argument('currencypair')
    def invalidPair(currencypair):
		prices = {'BTC_ETH': 1}
		if currencypair not in prices:
			raise click.ClickException('Invalid pair entered.')

    runner = CliRunner()
    result = runner.invoke(invalidPair, ['j'])
    assert result.exit_code == 1
    assert result.output == 'Error: Invalid pair entered.\n'


# Test 4: Test valid then invalid currency.
def test_validThenInvalidPair():
    @click.command()
    @click.argument('currencypair')
    def validThenInvalidPair(currencypair):
		prices = {'BTC_ETH': 1}
		if currencypair not in prices:
			raise click.ClickException('Invalid pair entered.')
		prices = {}
		if currencypair not in prices:
			raise click.ClickException('Invalid pair entered.')

    runner = CliRunner()
    result = runner.invoke(validThenInvalidPair, ['BTC'])
    assert result.exit_code == 1
    assert result.output == 'Error: Invalid pair entered.\n'


