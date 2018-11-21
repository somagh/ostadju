document.getElementById('id_search_profiles_form').addEventListener('input', function (e) {
    results = document.getElementById('autocomplete_results');
    fetch("http://localhost:8000/search_teachers_api?query=" + e.target.value).then(function (response) {
        return response.json()
    }).then(function (json) {
        results.innerHTML='';
        json.map(function (teacher) {
            results.innerHTML += '<a href="http://localhost:8000'+teacher.profile_url+'">' + teacher.first_name + ' ' + teacher.last_name + '</a>'
        })
    })
});