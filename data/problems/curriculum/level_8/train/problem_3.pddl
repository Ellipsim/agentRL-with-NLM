

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on-table b1)
(on b2 b10)
(on b3 b2)
(on b4 b3)
(on b5 b1)
(on-table b6)
(on b7 b8)
(on b8 b5)
(on-table b9)
(on b10 b7)
(clear b4)
(clear b6)
(clear b9)
)
(:goal
(and
(on b1 b2)
(on b3 b1)
(on b4 b9)
(on b6 b5)
(on b9 b7))
)
)


