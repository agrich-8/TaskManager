import UIKit

final class LoginRouter:PresenterToRouterLoginProtocol {
    
    static func createModule() -> LoginViewController {
        
        let loginViewController = LoginViewController()
        let loginPresenter: (ViewToPresenterLoginProtocol & InteractorToPresenterLoginProtocol) = LoginPresenter()
        loginViewController.presenter = loginPresenter
        loginViewController.presenter?.view = loginViewController
        loginViewController.presenter?.interactor = LoginInteractor()
        loginViewController.presenter?.router = LoginRouter()
        loginViewController.presenter?.interactor?.presenter = loginPresenter
        return loginViewController
    }
    
    func openRegisterView(navigationController: UINavigationController?) {
        
        let registerViewController = RegisterViewController()
        
        let registerPresenter: (ViewToPresenterRegisterProtocol & InteractorToPresenterRegisterProtocol) = RegisterPresenter()
        
        registerViewController.presenter = registerPresenter
        registerViewController.presenter?.view = registerViewController
        registerViewController.presenter?.interactor = RegisterIneractor()
        registerViewController.presenter?.router = RegisterRouter()
        registerViewController.presenter?.interactor?.presenter = registerPresenter
        
        navigationController?.pushViewController(registerViewController, animated: false)
    }
}
