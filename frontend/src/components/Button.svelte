<script>
    let name = 'Anais';
    function changeName() {
        if(name === 'Anais'){
            name = 'Parsa';
        }
        else{
            name = 'Anais';
        }
    }
    
</script>

<div>
    <button on:click={changeName}>
        {name}
    </button>
</div>