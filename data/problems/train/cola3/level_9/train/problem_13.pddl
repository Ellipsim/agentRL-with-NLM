

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(ontable b3)
(ontable b4)
(on b5 b7)
(on b6 b4)
(on b7 b3)
(ontable b8)
(on b9 b5)
(on b10 b1)
(clear b2)
(clear b8)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b8)
(on b2 b6)
(on b3 b2)
(on b4 b10)
(on b6 b4)
(on b7 b3)
(on b8 b5)
(on b9 b1)
(on b10 b9))
)
)


