console.log("Hello")

function getRecipe(event){
    event.preventDefault()
    console.log("Function Linked")
    let recipeForm =document.querySelector('#add_recipe')
    let recipeTableBody =document.querySelector('#recipe_table_body')
    console.log(recipeForm)
    let formData= new FormData(recipeForm)
    fetch("/api/recipe/create", {
        method:'post',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        recipeTableBody.innerHTML += ` 
        <tr>
            <td><input type="checkbox" id="ckmealplan" name="meal plan"></td>
            <td>${data.form.name}</td>
            <td>${data.form.cook_time}</td>
            <td>${data.poster}</td>
            <td><a href="/recipe/${data.recipe_id}/view">View Recipe</a>  
                <a href="recipe/${data.recipe_id}}/edit">Edit</a> | 
                <a href="/recipe/${data.recipe_id}}/delete">Delete</a>
            </td>
        </tr>
        `
    })
    .then(err => console.log(err))
}

function editRecipe(event){
    event.preventDefault()
    console.log("Function Linked")
    let recipeForm =document.querySelector('#edit_recipe')
    let recipeTableBody =document.querySelector('#recipe_info')
    console.log(recipeForm)
    let formData= new FormData(recipeForm)
    fetch("/api/recipe/"+ formData.get('id') +"/update", {
        method:'post',
        body: formData
    })
    .then(res => res.json())
    .then(data => 
    {
        console.log(data)
        recipeTableBody.innerHTML = `
        <div>
        <h1>${data.form.name}</h1>
        <p>Posted by: ${data.poster}</p>
        </div>
        <div>
                <p>Description:         ${data.form.description}</p>
                <p>Cook Time            ${data.form.cook_time}</p>
                <p>Instructions         ${data.form.instructions}</p>
                <p>Ingredients          ${data.form.ingredients}</p> 
                <p>Date Made            ${data.form.date_cooked}</p>
        </div>
        `
    })
    .then(err => console.log(err))
}