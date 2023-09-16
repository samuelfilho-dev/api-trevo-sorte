# API Trevo: A Django RESTful API


Este é um projeto que visa fornecer informações sobre o cadastro de usuários de sistema de compra de biletes De rifa. 
O projeto inclui uma API em Django Rest Framework que permite o acesso aos dados dos usuários com seus biletes de rifas
e o pagamento em formato PIX.

<p align="center">
     <a alt="Python">
        <img src="https://img.shields.io/badge/Python-v3.11-blue.svg" />
    </a>
    <a alt="PIP">
        <img src="https://img.shields.io/badge/PIP-v22.3.1-lightblue.svg" />
    </a>
     <a alt="Django">
        <img src="https://img.shields.io/badge/Django-v4.2.4-darkgreen.svg" />
    </a>
    <a alt="DRF">
        <img src="https://img.shields.io/badge/DRF-v3.14.0-orange.svg" />
    </a>
</p>

## Configuração

> Tenha instalado o Docker em sua maquina para configurar a API, caso tenha dúvida [Clique aqui!](https://docs.docker.com/engine/install/)

1. Clone o repositório: `git clone git@github.com:samuelfilho-dev/api-trevo-sorte.git`
2. Inicie o ambiente Docker: `docker-compose up`
3. Faças as Migrações:
   - `docker-compose exec web python manage.py migrate`
   - `docker-compose exec web python manage.py createsuperuser` 
4. Acesse `http://127.0.0.1:8000/`

> Request

```
curl --location 'http://127.0.0.1:8000/api/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Killua",
    "email": "killua@email.com",
    "phone": "1111-1111",
    "combo_number": 5,
    "password": "senha"
}'
```

> Response

```json
{
    "id": 8,
    "name": "Killua",
    "email": "killua@email.com",
    "phone": "1111-1111",
    "role": "user",
    "status": "pending",
    "create_at": "2023-09-16T18:04:10.601861Z",
    "update_at": "2023-09-16T18:04:11.035301Z",
    "raffles": [
        {
            "id": 3,
            "payment": {
                "id": 3,
                "status": "pending",
                "api_id": "63681908953",
                "value": "2.45",
                "qr_code": "00020126580014br.gov.bcb.pix0136ae9ef690-b01c-4e54-8bd4-62259369539d52040000530398654042.455802BR5908SNA_32646009Sao Paulo62240520mpqrinter636819089536304DDC8",
                "qr_code_base64": "iVBORw0KGgoAAAANSUhEUgAABWQAAAVkAQAAAAB79iscAAAI0UlEQVR42u3dS67bOBAFUO5A+98ld6BGgKRjs27RHgSNDnU8CPISSzp6s4v6cNx/0WcOWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWto/rx3r5/rxb7//+PX5cdWvv/26bPnbz69cr3d+fdD18yuv35v/PrIyaGlpaWlpaWlpaWlpH6K9XiNb++PrPV/vNF4Vv43z9SV//+/rL2jRtgxaWlpaWlpaWlpaWtoHaJcAucTBhVLSYRM+l6+UGHqFa0fA09LS0tLS0tLS0tLSPlS7JLxS7LvfX20p8Y0SLwv+fr8zLS0tLS0tLS0tLS0t7ful5X/bJLg0TV6lfldqf3d5SVpaWlpaWlpaWlpa2mdrM/67Cl3521uv5fIG5VbX5+ZPWlpaWlpaWlpaWlra07X7LSX/2R9/ZKcKLS0tLS0tLS0tLS3t36fNn1miXyrT5XrgCGtJao2wFPs2FlpaWlpaWlpaWlpa2rO1syS4xZOm3DYh8Cr5NK/xXwp7bbGPlpaWlpaWlpaWlpb2bG1JgjPnurTIZOnETIsj2/bO12haeKNLkbS0tLS0tLS0tLS0tCdqR9j7uEy0XcW95L/yY7tCcobmylmetu0RpaWlpaWlpaWlpaWlPU+bCnHtBpHEyxNtu9yZTnRL+09oaWlpaWlpaWlpaWlP1+bi3CyLHtuTsUuyHGVR/9J1mR5ZmjVpaWlpaWlpaWlpaWmfoi2AmXnFM7tRt6UTc4RhuxQg69FstLS0tLS0tLS0tLS0T9RuVobMkA7v8uU84Fbn4nLZL6toaWlpaWlpaWlpaWlP1i71trK8vzmcOi8oubqRuDZFtlmUlpaWlpaWlpaWlpb2KdrXm9RWyWxsrt10XbY9nlf4jQxaWlpaWlpaWlpaWtpnanOH5ZWjZF4c2QbNKx+PXSLsW3mQlpaWlpaWlpaWlpb2Idr21Ool642wmb8dYUuBdJb7lf8dH3dd0tLS0tLS0tLS0tLSnqYtG0nSypC6faR8787jb3kr5HxPjLssSktLS0tLS0tLS0tLe7526YiszZB5X0mt2i0LJtvezaX2V35ztLS0tLS0tLS0tLS0D9POvJskR8QZDlVLbZtXx7u77szmMlpaWlpaWlpaWlpa2vO1dx5hS7J96kszdeV+KXzW/f7bzEtLS0tLS0tLS0tLS3uUtoym3WEu7srdmeV1m07MDaURdCmSlpaWlpaWlpaWlpb2UG1aI7KEytIlOcs2kzYn5gc1Nb1wDgAtLS0tLS0tLS0tLe3J2n3XZd5XcpVyXu6XfHvGfqVJTqq0tLS0tLS0tLS0tLQP0I74SZ2TtRq33DjXCJey364UWKC0tLS0tLS0tLS0tLQP0L5W6MbYjcm17ZPNY9OsXF7jPzfPpaWlpaWlpaWlpaWlfYR2IZdey7vMrC3QFEPL4dl3Lue119LS0tLS0tLS0tLS0j5Ee+eBtPTYdsotHXadzwGYoSjY7PenpaWlpaWlpaWlpaV9hDZtC8kbIEd32PWVry3rS5Zf0P5aWlpaWlpaWlpaWlraR2nTDNxmZ+TdJcbdq5X2zn2epKWlpaWlpaWlpaWlfZR2477yIpMEKEXBkXeTpJpeuyeFlpaWlpaWlpaWlpb2fG1a3l/H1TarRepI3DJsl5o1UypdBLS0tLS0tLS0tLS0tA/RjnB0dYqIV2jRHO8VuuVUtt1leevJXcInLS0tLS0tLS0tLS3t+dprc4Da8r3lNZYk2LZolmLf/gbbrktaWlpaWlpaWlpaWtpztUsL5H4GbnNs2n7obb7Pzy1p8yogWlpaWlpaWlpaWlraR2jzsxO0jZJNPXB5yXRudntGNi0tLS0tLS0tLS0t7UO0zVaREgfvT12XOTvud5iMEjk/pEhaWlpaWlpaWlpaWtrTtLmIN8NNRtcqeXWBdHZ7Kevha192XdLS0tLS0tLS0tLS0p6nzeGujZKzfK88Yreg5Is+zc87VWhpaWlpaWlpaWlpaY/SlpG4GQ7A3pfp6tLJfSBNu/xT8yctLS0tLS0tLS0tLe1ztO3M2gb6lvXy0Wx1YG55v+Wdu3k8WlpaWlpaWlpaWlras7Xtksi6PCT/W6ruNSspF3wroKWlpaWlpaWlpaWlfZL2fk+MzWnUaaPkVyW+mQ/KLi2ay61oaWlpaWlpaWlpaWmfos2nYI/wsFEOu26X/O/H6cpdxtddl7S0tLS0tLS0tLS0tGdrl9Ld/f7Eq0zNpZbK8rp3CJ/1QWX1yUVLS0tLS0tLS0tLS/sQbV5L8mbMNbiRWyXTMpJUtduk0pJPaWlpaWlpaWlpaWlpT9bmwbWr7CspaTM1SN75VqnHM+38z1fQ0tLS0tLS0tLS0tKerW0bH5dBuCX15RUkS0RclpukA7Dr1NyHrf60tLS0tLS0tLS0tLTnae+y3jHNxZWHNVXAUs5ri33pkfc3O1VoaWlpaWlpaWlpaWmP0pYJtFmWh2zKeQlaezfbNyiVwRF3/tPS0tLS0tLS0tLS0j5AO8KJaSNnx1QFLIEwTb59ESWv71IkLS0tLS0tLS0tLS3tQdr0+VR+S1XAdgZuhr0m+2bNezcNR0tLS0tLS0tLS0tLe5o2B7mRA1+Jksv7pcUjzbVl2K5eS0tLS0tLS0tLS0tL+xDt/rHtppHZLS1JifF6LyPO/OLfpEhaWlpaWlpaWlpaWtojtaXnsR2Eq7dLpcDSzzm/uiyv9qelpaWlpaWlpaWlpX2o9tOmkebL7fL+9tCA9vA1WlpaWlpaWlpaWlraZ2vTqFteK5nG5K7wY11akngfdqrQ0tLS0tLS0tLS0tIeqU1dl2norT0juzRhpnG6trlyhn0ltLS0tLS0tLS0tLS0z9HWxselGpfC4hICl0C6fK9NoLkKuO26pKWlpaWlpaWlpaWlPU37///Q0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0v4x7T/F4RasFpb+VwAAAABJRU5ErkJggg==",
                "url": "https://www.mercadopago.com.br/payments/63681908953/ticket?caller_id=1482654968&hash=d36a8fcd-58de-4284-9f7b-7d146223921a",
                "date_expiration": "2023-09-17T14:04:11.879-04:00",
                "create_at": "2023-09-16T18:04:12.661614Z",
                "update_at": "2023-09-16T18:04:12.661614Z"
            },
            "status": "active",
            "combo_name": "Combo Do Killua - 5 Números",
            "combo_number": 5,
            "raffle": [
                7498,
                74878,
                57282,
                41270,
                70198
            ],
            "user": 8
        }
    ]
}
```
---

## Documentação do Swagger

A documentação da API pode ser encontrada no Swagger. Para visualizá-la,
acesse: [Documentação do Swagger](http://127.0.0.1:8000/swagger/).


## Licença

Este projeto está licenciado sob a licença Comercial. Consulte o
arquivo [(LICENSE)](https://github.com/samuelfilho-dev/api-trevo-sorte/blob/main/LICENSE).

> ⚠️ Essa API está em licença comercial, não use sem autorização do Autor

## Autor

<table>
  <tr>
    <td align="center"><a href="https://github.com/samuelfilho-dev"><img src="https://avatars.githubusercontent.com/u/81279868?s=400&u=89e596d8d5cc674251c908e45fa47a37db0db3a0&v=4" width="100px;" alt=""/><br/><strong>Samuel Filho</strong></a><br/><a href="https://www.linkedin.com/in/samuelfilho-dev/">LinkedIn</a></td>
  </tr>
</table>