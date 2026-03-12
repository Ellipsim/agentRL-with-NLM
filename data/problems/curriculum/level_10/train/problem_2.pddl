

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b12)
(on b2 b7)
(on-table b3)
(on-table b4)
(on b5 b6)
(on b6 b11)
(on b7 b4)
(on-table b8)
(on b9 b10)
(on b10 b1)
(on b11 b3)
(on-table b12)
(clear b2)
(clear b5)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b6)
(on b2 b11)
(on b3 b1)
(on b4 b3)
(on b10 b9)
(on b11 b4)
(on b12 b5))
)
)


