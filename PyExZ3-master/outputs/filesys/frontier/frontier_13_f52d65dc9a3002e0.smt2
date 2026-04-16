(set-logic ALL)
; Constraint ID: f52d65dc9a3002e0
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60454)) (False)
(assert (not (= x 60454)))

; Query: ((== x 60455)) (False)
(assert (not (not (= x 60455))))

(check-sat)
(get-model)
