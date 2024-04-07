let dynamicContent = "";
let restaurantStats = "";

const originalButtonStyles = {};
const buttons = document.querySelectorAll('#nav-buttons button');
buttons.forEach(button => {
	originalButtonStyles[button.id] = {
		backgroundColor: button.style.backgroundColor,
		color: button.style.color,
		border: button.style.border
	};
});

function updateScreen(content) {
	dynamicContent = content;

	if (content == "Iggy's Market" || content == "Boulder") {
		restaurantStats = "Dine in, Low Wait Time";
	} else {
		restaurantStats = "Dine in, Medium Wait Time";
	}

	document.querySelector('main').style.display = 'none';
	document.getElementById('hello-screen').style.display = 'block';
	document.getElementById('dynamicContent').innerText = dynamicContent;
	document.getElementById('restaurantStats').innerText = restaurantStats;

	resetButtonStyles();

	hideThirdScreen(); // Hide the third screen when updating to the hello screen

	localStorage.setItem('currentScreen', 'hello-screen');
}

function selectFoodItem(item) {
	document.getElementById('hello-screen').style.display = 'none';
	document.getElementById('third-screen').style.display = 'block';
	document.getElementById('dynamicContentThird').innerText = item;
	localStorage.setItem('currentScreen', 'third-screen');
}

function goBack() {
	document.querySelector('main').style.display = 'block';
	document.getElementById('hello-screen').style.display = 'none';
	document.getElementById('third-screen').style.display = 'none';
	resetButtonStyles();
	localStorage.setItem('currentScreen', 'original-page');
}

function goBackToSecondScreen() {
	document.getElementById('hello-screen').style.display = 'block';
	document.getElementById('third-screen').style.display = 'none';
	localStorage.setItem('currentScreen', 'hello-screen');
}

function resetButtonStyles() {
	const buttons = document.querySelectorAll('#nav-buttons button');
	buttons.forEach(button => {
		const originalStyles = originalButtonStyles[button.id];
		button.style.backgroundColor = originalStyles.backgroundColor;
		button.style.color = originalStyles.color;
		button.style.border = originalStyles.border;
	});
}

function hideThirdScreen() {
	document.getElementById('third-screen').style.display = 'none';
}

function hideThirdScreenOnMenuClick() {
	document.getElementById('third-screen').style.display = 'none';
}

document.getElementById('iggy-market').addEventListener('click', () => {
	updateScreen("Iggy's Market");
	hideThirdScreenOnMenuClick();
});
document.getElementById('boulder').addEventListener('click', () => {
	updateScreen("Boulder");
	hideThirdScreenOnMenuClick();
});
document.getElementById('boulder-2').addEventListener('click', () => {
	updateScreen("Boulder 2.0");
	hideThirdScreenOnMenuClick();
});

function showScreenFromLocalStorage() {
	goBack(); // Always default to the home screen
}

window.onload = showScreenFromLocalStorage;