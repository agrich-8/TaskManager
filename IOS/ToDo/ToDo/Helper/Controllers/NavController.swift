import UIKit

class NavController:UINavigationController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.configure()
    }
}

extension NavController {
    private func configure() {
        view.backgroundColor = .white
        navigationBar.standardAppearance.titleTextAttributes = [.font:UIFont.boldSystemFont(ofSize: 28)]
    }
}
