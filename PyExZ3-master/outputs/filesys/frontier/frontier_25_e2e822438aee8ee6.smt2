(set-logic ALL)
; Constraint ID: e2e822438aee8ee6
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60622)) (False)
(assert (not (= x 60622)))

; Query: ((== x 60623)) (False)
(assert (not (not (= x 60623))))

(check-sat)
(get-model)
