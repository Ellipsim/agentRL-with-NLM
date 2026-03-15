

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b7)
(on b3 b9)
(on b4 b10)
(on-table b5)
(on b6 b3)
(on b7 b8)
(on b8 b5)
(on b9 b4)
(on-table b10)
(on b11 b1)
(on-table b12)
(clear b2)
(clear b11)
(clear b12)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b5)
(on b6 b4)
(on b7 b8)
(on b8 b12)
(on b9 b10)
(on b12 b1))
)
)


