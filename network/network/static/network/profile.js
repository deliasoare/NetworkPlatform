document.addEventListener('DOMContentLoaded', function() {
    const popup = document.querySelector('#popupFollowing');
    document.querySelector('#followers').onclick = function() {
        document.querySelector('#popupFollowers').style.display = 'block';   
    }
    document.querySelector('.closeFollowers').onclick = function() {
        document.querySelector('#popupFollowers').style.display = 'none'
    }
    document.querySelector('.closeFollowing').onclick = function() {
        popup.style.display = 'none'
    }
    window.onclick = function(event) {
        if (event.target == document.querySelector('#popupFollowers')) {
            document.querySelector('#popupFollowers').style.display = 'none';
        }
        else if (event.target == popup)
            popup.style.display = 'none';
    }
    
    document.querySelector('#following').onclick = function() {
        popup.style.display = 'block';
    }

})