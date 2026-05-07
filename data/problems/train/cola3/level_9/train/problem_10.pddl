

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(ontable b3)
(on b4 b2)
(ontable b5)
(on b6 b5)
(ontable b7)
(on b8 b10)
(on b9 b4)
(on b10 b6)
(clear b3)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b9)
(on b2 b6)
(on b3 b8)
(on b4 b7)
(on b5 b4)
(on b8 b2)
(on b9 b5))
)
)


