import pegadados as p
import moedas as m

h_atual = p.updates(True)
tempo = p.delta(h_atual)

if tempo > 12:  # Faz a atualização dos dados, se necessária
    p.getcoins()

usd_real, usd_guarani, usd_peso = m.usd_cot(), m.usd_cot('Paraguai'), m.usd_cot('Argentina')

print(f'    Cotação do dia\n'
      f'{usd_real}\n'
      f'{usd_guarani}\n'
      f'{usd_peso}')
