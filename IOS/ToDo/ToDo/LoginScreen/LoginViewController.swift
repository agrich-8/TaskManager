import UIKit

final class LoginViewController:BaseViewController {
    var presenter:(ViewToPresenterLoginProtocol & InteractorToPresenterLoginProtocol)?
    
    let loginButton = UIButton()
    let registerButton = UIButton()
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    override func viewDidLayoutSubviews() {
        loginButton.widthAnchor.constraint(equalToConstant: registerButton.bounds.width).isActive = true
    }
    
}

extension LoginViewController {
    override func addViews() {
        self.view.addView(loginButton)
        self.view.addView(registerButton)
    }
    
    override func layoutViews() {
        NSLayoutConstraint.activate([
            loginButton.centerXAnchor.constraint(equalTo: self.view.centerXAnchor, constant: 0),
            loginButton.centerYAnchor.constraint(equalTo: self.view.centerYAnchor, constant: -40),
            registerButton.centerXAnchor.constraint(equalTo: self.view.centerXAnchor, constant: 0),
            registerButton.centerYAnchor.constraint(equalTo: self.view.centerYAnchor, constant: 40)
        ])
    }
    
    override func configure() {
        title = "Login"
        
        loginButton.addTarget(self, action: #selector(loginButtonTapped), for: .touchUpInside)
        registerButton.addTarget(self, action: #selector(registerButtonTapped), for: .touchUpInside)
        
        self.configureButton(button: loginButton, text: "Sign in")
        self.configureButton(button: registerButton, text: "Register")
    }
}

extension LoginViewController {
    private func configureButton(button:UIButton, text:String) {
        button.setTitle(text, for: .normal)
        button.layer.masksToBounds = true
        button.layer.cornerRadius = 8
        button.backgroundColor = .systemOrange
        button.setTitleColor(.white, for: .normal)
        button.contentEdgeInsets = UIEdgeInsets(top: 15, left: 30, bottom: 15, right: 30)
    }
}


extension LoginViewController {
    @objc private func registerButtonTapped(_ sender:UIButton) {
        presenter?.touchRegisterButton(navigationController: navigationController)
    }
    
    @objc private func loginButtonTapped(_ sender:UIButton) {
        
    }
}

extension LoginViewController:PresenterToViewLoginProtocol {
    
}
