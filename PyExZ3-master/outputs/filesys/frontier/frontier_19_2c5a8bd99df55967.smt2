(set-logic ALL)
; Constraint ID: 2c5a8bd99df55967
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60388)) (False)
(assert (not (= x 60388)))

; Query: ((== x 60389)) (False)
(assert (not (not (= x 60389))))

(check-sat)
(get-model)
