import UIKit

class RegisterViewController: BaseViewController {
    var presenter:(ViewToPresenterRegisterProtocol & InteractorToPresenterRegisterProtocol)?
    
    let scrollView = UIScrollView()
    let loginTextField = UITextField()
    let mailTextField = UITextField()
    let passwordTextField = UITextField()
    let confirmPasswordTextField = UITextField()
    let loginLabel = UILabel()
    let mailLabel = UILabel()
    let passwordLabel = UILabel()
    let confirmPasswordLabel = UILabel()
    let confirmButton = UIButton()
    let errorLabel = UILabel()
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
}

extension RegisterViewController {
    
    
    override func addViews() {
        self.view.addView(scrollView)
        scrollView.addSubview(loginLabel)
        scrollView.addSubview(loginTextField)
        scrollView.addSubview(mailLabel)
        scrollView.addSubview(mailTextField)
        scrollView.addSubview(passwordLabel)
        scrollView.addSubview(passwordTextField)
        scrollView.addSubview(confirmPasswordLabel)
        scrollView.addSubview(confirmPasswordTextField)
        scrollView.addSubview(confirmButton)

    }
    
    override func configure() {
        title = "Register"
        
        scrollView.contentSize = CGSize(width: UIScreen.main.bounds.width, height: UIScreen.main.bounds.height)
        scrollView.showsVerticalScrollIndicator = false
        
        self.configureLabel(label: loginLabel, text: "Login:")
        self.configureLabel(label: mailLabel, text: "Mail:")
        self.configureLabel(label: passwordLabel, text: "Password:")
        self.configureLabel(label: confirmPasswordLabel, text: "Confirm password:")
        
        self.configureTextField(textField: loginTextField, placeholderText: "Login")
        self.configureTextField(textField: mailTextField, placeholderText: "Mail")
        self.configureTextField(textField: passwordTextField, placeholderText: "Password",isSecury: true)
        self.configureTextField(textField: confirmPasswordTextField, placeholderText: "Password",isSecury: true)
        
        confirmButton.setTitle("Confirm", for: .normal)
        confirmButton.layer.masksToBounds = true
        confirmButton.isEnabled = false
        confirmButton.layer.cornerRadius = 13
        confirmButton.backgroundColor = .gray
        confirmButton.setTitleColor(.white, for: .normal)
        confirmButton.contentEdgeInsets = UIEdgeInsets(top: 10, left: 20, bottom: 10, right: 20)
        confirmButton.addTarget(self, action: #selector(confirmButtonTapped), for: .touchUpInside)
    }
    
    override func layoutViews() {
        NSLayoutConstraint.activate([
            scrollView.topAnchor.constraint(equalTo: self.view.safeAreaLayoutGuide.topAnchor, constant: 0),
            scrollView.leftAnchor.constraint(equalTo: self.view.safeAreaLayoutGuide.leftAnchor, constant: 0),
            scrollView.rightAnchor.constraint(equalTo: self.view.safeAreaLayoutGuide.rightAnchor, constant: 0),
            scrollView.bottomAnchor.constraint(equalTo: self.view.safeAreaLayoutGuide.bottomAnchor, constant: 0),
            loginTextField.centerYAnchor.constraint(equalTo: scrollView.centerYAnchor, constant: -50),
            loginTextField.rightAnchor.constraint(equalTo: self.view.safeAreaLayoutGuide.rightAnchor,constant: -10),
            loginTextField.heightAnchor.constraint(equalToConstant: 30),
           loginTextField.leftAnchor.constraint(equalTo: loginLabel.rightAnchor, constant: 10),
            loginTextField.widthAnchor.constraint(equalToConstant: 200),
            loginLabel.centerYAnchor.constraint(equalTo: loginTextField.centerYAnchor),
            loginLabel.leftAnchor.constraint(equalTo: scrollView.leftAnchor,constant: 20),
            mailTextField.rightAnchor.constraint(equalTo: loginTextField.rightAnchor),
            mailTextField.leftAnchor.constraint(equalTo: loginTextField.leftAnchor),
            mailTextField.topAnchor.constraint(equalTo: loginTextField.bottomAnchor,constant: 20),
            mailTextField.heightAnchor.constraint(equalTo: loginTextField.heightAnchor),
            mailLabel.centerYAnchor.constraint(equalTo: mailTextField.centerYAnchor),
            mailLabel.leftAnchor.constraint(equalTo: loginLabel.leftAnchor),
            mailLabel.rightAnchor.constraint(equalTo: loginTextField.leftAnchor,constant: -5),
            passwordTextField.rightAnchor.constraint(equalTo: loginTextField.rightAnchor),
            passwordTextField.leftAnchor.constraint(equalTo: loginTextField.leftAnchor),
            passwordTextField.topAnchor.constraint(equalTo: mailTextField.bottomAnchor,constant: 20),
            passwordTextField.heightAnchor.constraint(equalTo: loginTextField.heightAnchor),
            passwordLabel.centerYAnchor.constraint(equalTo: passwordTextField.centerYAnchor),
            passwordLabel.leftAnchor.constraint(equalTo: loginLabel.leftAnchor),
            passwordLabel.rightAnchor.constraint(equalTo: passwordTextField.leftAnchor,constant: -5),
            confirmPasswordTextField.rightAnchor.constraint(equalTo: loginTextField.rightAnchor),
            confirmPasswordTextField.leftAnchor.constraint(equalTo: loginTextField.leftAnchor),
            confirmPasswordTextField.topAnchor.constraint(equalTo: passwordTextField.bottomAnchor,constant: 20),
            confirmPasswordTextField.heightAnchor.constraint(equalTo: loginTextField.heightAnchor),
            confirmPasswordLabel.centerYAnchor.constraint(equalTo: confirmPasswordTextField.centerYAnchor),
            confirmPasswordLabel.leftAnchor.constraint(equalTo: loginLabel.leftAnchor),
            confirmButton.topAnchor.constraint(equalTo: confirmPasswordTextField.bottomAnchor,constant: 20),
            confirmButton.centerXAnchor.constraint(equalTo: scrollView.centerXAnchor)
        ])
    }
}


extension RegisterViewController {
    private func configureLabel(label:UILabel, text:String) {
        label.text = text
        label.textColor = .systemOrange
        label.font = .boldSystemFont(ofSize: 13)
    }
    
    private func configureTextField(textField:UITextField,placeholderText:String, isSecury:Bool = false) {
        textField.isSecureTextEntry = isSecury
        textField.placeholder = placeholderText
        textField.layer.borderWidth = 1
        textField.layer.masksToBounds = true
        textField.layer.borderColor = UIColor.black.cgColor
        textField.layer.cornerRadius = 6
        textField.delegate = self
        textField.font = UIFont.systemFont(ofSize: 15)
        textField.borderStyle = UITextField.BorderStyle.roundedRect
        textField.autocorrectionType = UITextAutocorrectionType.no
        textField.keyboardType = UIKeyboardType.default
        textField.returnKeyType = UIReturnKeyType.done
        textField.clearButtonMode = UITextField.ViewMode.whileEditing;
        textField.contentVerticalAlignment = UIControl.ContentVerticalAlignment.center
    }
}

extension RegisterViewController {
    @objc private func confirmButtonTapped(_ sender:UIButton) {
        self.removeErrorState()
        presenter?.userTapConfirmButton()
    }
}


//MARK: - TextFieldDelegate
extension RegisterViewController:UITextFieldDelegate {
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    func textFieldDidEndEditing(_ textField: UITextField) {
        switch textField {
        case loginTextField:
            presenter?.setLogin(login: textField.text)
        case mailTextField:
            presenter?.setMail(mail: textField.text)
        case passwordTextField:
            presenter?.setPassword(password: textField.text)
        case confirmPasswordTextField:
            presenter?.checkConfirmPassword(confirmPassword: textField.text)
        default:
            return
        }
    }
    
    func textFieldShouldClear(_ textField: UITextField) -> Bool {
        self.removeErrorState()
        switch textField {
        case loginTextField:
            presenter?.setLogin(login: textField.text)
        case mailTextField:
            presenter?.setMail(mail: textField.text)
        case passwordTextField:
            presenter?.setPassword(password: textField.text)
        case confirmPasswordTextField:
            presenter?.checkConfirmPassword(confirmPassword: textField.text)
        default:
            break
        }
        return true
    }
    
}

//MARK: - PresenterToView
extension RegisterViewController:PresenterToViewRegisterProtocol {
    func onFailureRegistered(errorText: String) {
        let alert = UIAlertController(title: "Error", message: errorText, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
        present(alert,animated: true)
    }
    
    func enableConfirmButton() {
        self.confirmButton.isEnabled = true
        self.confirmButton.backgroundColor = .systemOrange
    }
    
    func errorRegister(errorText: String) {
        self.setupErrorLabel(errorText: errorText)
        self.disableConfirmButton()
    }
    
    func errorSimilarPassword() {
        self.confirmPasswordTextField.layer.borderColor = UIColor.red.cgColor
        self.confirmPasswordTextField.placeholder = "Passwords dont match"
        self.disableConfirmButton()
    }
}

extension RegisterViewController {
    private func setupErrorLabel(errorText:String) {
        errorLabel.translatesAutoresizingMaskIntoConstraints = false
        errorLabel.text = errorText
        errorLabel.textColor = .red
        errorLabel.font = .systemFont(ofSize: 15)
        self.scrollView.addSubview(errorLabel)
        
        NSLayoutConstraint.activate([
            errorLabel.centerXAnchor.constraint(equalTo: self.confirmButton.centerXAnchor),
            errorLabel.topAnchor.constraint(equalTo: self.confirmButton.bottomAnchor, constant: 15)
        ])
    }
    
    private func removeErrorState() {
        self.errorLabel.removeFromSuperview()
        self.confirmPasswordTextField.layer.borderColor = UIColor.black.cgColor
        self.confirmPasswordTextField.placeholder = "Password"
    }
    
    private func disableConfirmButton() {
        confirmButton.isEnabled = false
        confirmButton.backgroundColor = .gray
    }
}
