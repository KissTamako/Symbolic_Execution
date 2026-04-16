(set-logic ALL)
; Constraint ID: 0f60aaf3131d5497
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60022)) (False)
(assert (not (= x 60022)))

; Query: ((== x 60023)) (False)
(assert (not (not (= x 60023))))

(check-sat)
(get-model)
