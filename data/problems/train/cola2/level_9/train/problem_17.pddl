

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b10)
(ontable b2)
(on b3 b6)
(ontable b4)
(on b5 b2)
(on b6 b4)
(on b7 b1)
(ontable b8)
(on b9 b3)
(on b10 b8)
(clear b5)
(clear b7)
(clear b9)
)
(:goal
(and
(on b3 b8)
(on b4 b7)
(on b5 b1)
(on b7 b5)
(on b8 b9)
(on b10 b4))
)
)


