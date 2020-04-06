console.log('Hello world',window.location.href);
// console.log(window.location.href.split("/"));
if(window.location.href.split("/").includes("notes")){
    // console.log('Hello notes');
    let updateElements=document.getElementsByClassName('update');
    // console.log(updateElements);
    Array.from(updateElements).forEach(function (updateEle) {
        updateEle.addEventListener("click",function(e) {
            let form=document.createElement('form');
            form.action=`/notes/update/${e.target.dataset.userid}/${e.target.id}`;
            form.method="POST";
            let textEle=document.createElement('input');
            textEle.type='text';
            textEle.name='content';
            textEle.class='form-control';
            textEle.placeholder=updateEle.innerText;
            form.appendChild(textEle)
            let td=document.createElement('td');
            td.appendChild(form);
            updateEle.replaceWith(td);
            textEle.addEventListener('blur',function(e){
                form.submit();
            });
        })
        updateEle.addEventListener("mouseover",function(e){
            e.target.style.cursor='pointer';
        });
    })
}