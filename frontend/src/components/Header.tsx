type HeaderProps = {
    titolo: string,
    sottotitolo: string
}

function Header({titolo, sottotitolo}: HeaderProps) {
    return (
    <>
      <h1>
          {titolo}
      </h1>
      <p>
          {sottotitolo}
      </p>
    </>
    )
}

export default Header
