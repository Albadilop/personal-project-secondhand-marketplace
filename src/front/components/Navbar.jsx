import { Link } from "react-router-dom";
import logo from "../assets/img/logo.png";

export const Navbar = () => {

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					    <a class="navbar-brand" href="#">
      <img src={logo} alt="Logo" width="40" height="34" class="d-inline-block align-text-top "/>
      The Second Life Hub
    </a>
				</Link>
				<div className="ml-auto">
					<nav class="navbar bg-body-tertiary">
						<div class="container-fluid">
							<form class="d-flex" role="search">
						
							
								<input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
						
								<button class="btn btn-outline-success" type="submit">Search</button>
								
							</form>
							
						</div>
					</nav>
				</div>
				<div>

				<button type="button" class="btn btn-primary me-4">Register or Log-In</button>
				
				<button type="button" class="btn btn-primary">Sell</button>
				</div>
			</div>
		</nav>
	);
};