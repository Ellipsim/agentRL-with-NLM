

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b4)
(on b2 b7)
(on b3 b1)
(on b4 b2)
(on b5 b9)
(on-table b6)
(on b7 b10)
(on b8 b6)
(on b9 b8)
(on-table b10)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b6)
(on b2 b7)
(on b3 b5)
(on b5 b2)
(on b6 b3)
(on b7 b4)
(on b9 b8))
)
)


