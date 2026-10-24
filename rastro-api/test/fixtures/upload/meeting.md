Marina: Bom, pessoal, a ideia hoje é decidir qual banco vamos usar no ambiente de produção. Eu conversei com o time de infraestrutura e eles sugeriram PostgreSQL.

Rafael: Para mim faz sentido. A gente já usa PostgreSQL em outros serviços e o time conhece bem as ferramentas de backup e monitoramento.

João: Eu só queria confirmar se a extensão para busca vetorial está disponível no ambiente que vamos contratar. Não queria depender de outro banco só por causa disso.

Marina: Confirmei isso ontem. O ambiente suporta pgvector, então conseguimos manter os dados dos documentos e os vetores no mesmo banco.

Rafael: Nesse caso, minha sugestão é seguir com PostgreSQL e deixar a configuração do ambiente pronta antes de começar a indexação.

João: Fechado. Eu posso preparar a configuração local e documentar as variáveis necessárias.

Marina: Ótimo. Então fica decidido: vamos usar PostgreSQL. João prepara o ambiente local até sexta-feira e Rafael valida o monitoramento depois.
