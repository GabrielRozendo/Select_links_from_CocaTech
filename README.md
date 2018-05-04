# Select links from CocaTech

Crawler em python buscando os links do [CocaTech](https://cocatech.com.br/) e salvando em um banco de dados [Cosmos DB no Azure](https://azure.microsoft.com/services/cosmos-db/)

Utilizando [Angular](https://angular.io/) para exibir essas informações vindas do [Azure](https://azure.microsoft.com)

e também enviando cada novo link através de um bot no [Telegram](https://telegram.me/)


## Ideia

Como nem sempre dá para pegar os links escutando os podcasts do Coca e as vezes tem links úteis e/ou de promoções, pegar todas e listá-las, além de enviar via telegram...

### Unindo aprendizado com necessidade
Dessa forma consigo praticar Python (e seus diversos recursos), Mongo DB, aproveitar a conta que já tenho no Azure, aproveitar o Telegram que já uso frequentemente e depois, quando quiser ver, posso acessar a página feita com Angular (que também serve de aprendizado).
Isso tudo além de conseguir o objetivo de ter os links divulgados mesmo antes de escutar e salvos pra posteriormente...


## Tecnologias utilizadas

* Python - Crawler lendo o Feed RSS e descobrindo o que há de novo, salvando os novos no DB
* Cosmos DB no Azure (Mongo DB)
* Bot no Telegram enviando cada novo link encontrado
* Angular para exibir os links


## Etapas

1: ler os feed rss ✅

2: ler a página e pegar os links ⚠️

3: criar o cosmos db ✅ --> Alterar para utilizar SQL, pois está muito caro!

4: salvar esses dados no azure ✅

5: exibir via angular ❌

6: enviar via bot do Telegram ✅

## Author

* **Gabriel Oliveira Rozendo**