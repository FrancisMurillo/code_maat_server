(require 'prodigy)

(with-eval-after-load 'prodigy
  (defconst fbn/code-maat-viewer-backend-service-name "code-maat-viewer-backend"
    "The code-maat-viewer backend service name.")

  ;; Tags
  (prodigy-define-tag
    :name 'code-maat-viewer-backend
    :cwd (projectile-project-root))

  (prodigy-define-tag
    :name 'code-maater-pyenv
    :command "./code-maater/bin/python")


  (fn/prodigy-define-service
   :name fbn/code-maat-viewer-backend-service-name
   :tags '(code-maat-viewer-backend code-maater-pyenv)
   :args `("app.py")

   ;; Custom Binding
   :bind-command-name "code-maat-viewer-backend"
   :bind-map fn/prodigy-map
   :bind (kbd "c c"))

  (prodigy-start-service (prodigy-find-service fbn/code-maat-viewer-backend-service-name)))
