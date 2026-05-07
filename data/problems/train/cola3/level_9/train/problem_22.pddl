

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b10)
(on b3 b1)
(on b4 b2)
(on b5 b6)
(on b6 b3)
(on b7 b4)
(on b8 b5)
(ontable b9)
(ontable b10)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b8)
(on b2 b3)
(on b3 b6)
(on b5 b1)
(on b6 b4)
(on b7 b5)
(on b8 b9)
(on b9 b10))
)
)


