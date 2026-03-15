

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b11)
(on-table b2)
(on b3 b4)
(on b4 b8)
(on b5 b2)
(on b6 b9)
(on-table b7)
(on b8 b13)
(on b9 b5)
(on b10 b3)
(on b11 b12)
(on-table b12)
(on b13 b7)
(clear b1)
(clear b6)
(clear b10)
)
(:goal
(and
(on b2 b13)
(on b4 b10)
(on b5 b2)
(on b6 b7)
(on b7 b4)
(on b9 b3)
(on b10 b1)
(on b11 b9))
)
)


