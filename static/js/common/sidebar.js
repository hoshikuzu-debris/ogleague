const sidebarToggleTop = document.getElementById('sidebarToggleTop');

let sidebarIsActive = false;

sidebarToggleTop.addEventListener('click', function(){
    if(sidebarIsActive)  {
        document.getElementById('sidebar-wrapper').style.display = 'none';
        sidebarIsActive = false;
    } else {
        document.getElementById('sidebar-wrapper').classList.remove('d-none');
        document.getElementById('sidebar-wrapper').style.display = 'flex';
        sidebarIsActive = true;
    }
});
