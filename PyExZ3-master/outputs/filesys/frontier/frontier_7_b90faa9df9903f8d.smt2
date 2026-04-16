(set-logic ALL)
; Constraint ID: b90faa9df9903f8d
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60670)) (False)
(assert (not (= x 60670)))

; Query: ((== x 60671)) (False)
(assert (not (not (= x 60671))))

(check-sat)
(get-model)
