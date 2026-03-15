

(define (problem BW-rand-14)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b14)
(on b3 b10)
(on b4 b13)
(on b5 b11)
(on-table b6)
(on b7 b9)
(on b8 b4)
(on-table b9)
(on b10 b5)
(on b11 b6)
(on b12 b1)
(on b13 b12)
(on-table b14)
(clear b3)
(clear b7)
(clear b8)
)
(:goal
(and
(on b4 b10)
(on b5 b9)
(on b8 b2)
(on b9 b8)
(on b10 b6)
(on b11 b5)
(on b13 b7)
(on b14 b1))
)
)


