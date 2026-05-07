

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b3)
(on b3 b10)
(on b4 b2)
(on b5 b9)
(ontable b6)
(on b7 b8)
(on b8 b4)
(on b9 b6)
(ontable b10)
(clear b1)
(clear b7)
)
(:goal
(and
(on b2 b3)
(on b3 b4)
(on b4 b10)
(on b5 b1)
(on b8 b9)
(on b9 b5)
(on b10 b7))
)
)


