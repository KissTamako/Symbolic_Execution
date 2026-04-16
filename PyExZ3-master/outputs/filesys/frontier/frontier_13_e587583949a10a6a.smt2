(set-logic ALL)
; Constraint ID: e587583949a10a6a
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59629)) (False)
(assert (not (= x 59629)))

; Query: ((== x 59630)) (False)
(assert (not (not (= x 59630))))

(check-sat)
(get-model)
