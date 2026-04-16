(set-logic ALL)
; Constraint ID: 1ab11c1d77f37725
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59932)) (False)
(assert (not (= x 59932)))

; Query: ((== x 59933)) (False)
(assert (not (not (= x 59933))))

(check-sat)
(get-model)
